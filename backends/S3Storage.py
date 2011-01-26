import os, time, logging, gzip
from mimetypes import guess_type
from time import mktime
from email.utils import parsedate
import urllib
try:
	from cStringIO import StringIO
except ImportError:
	from StringIO import StringIO

from django.conf import settings	
from django.core.exceptions import ImproperlyConfigured
from django.utils.http import urlquote
from django.core.files.base import File
from django.core.files.storage import Storage
from django.utils.encoding import force_unicode
from django.utils.functional import curry
from django.core.cache import cache

ACCESS_KEY_NAME = 'AWS_ACCESS_KEY_ID'
SECRET_KEY_NAME = 'AWS_SECRET_ACCESS_KEY'	
AWS_HEADERS = 'AWS_HEADERS'

GZIP_FILE_TYPES = ('text/css','text/javascript',)

try:
	from backends.S3 import AWSAuthConnection, QueryStringAuthGenerator
except ImportError:	
	raise ImproperlyConfigured, "Could not load amazon's S3 bindings.\
	\nSee http://developer.amazonwebservices.com/connect/entry.jspa?externalID=134"


# Helps S3Storage.exists make fewer S3 calls, on grounds that if the file
# existed some time ago, it probably still exists
SKIP_CHECKING_IF_FILE_EXISTS_TIMEOUT = 60 * 60 * 24 * 7 * 3 # Cache for 3 weeks


def _normalize_file_name(name):
	"""
	Normalize filenames to use forward slashes, even on Windows
	
	When uploading files on Windows Django will send the original filenames
	(with back slashes) to the chosen Storage backend on save. Django will then
	overwrite the filename (replacing back slashes with forward slashes) without
	notifying the said Storage backend - leading to a huge pile of hard to find
	bugs. 
	"""
	return force_unicode(name.replace('\\', '/'))


class S3Storage(Storage):
	"""Amazon Simple Storage Service"""

	def __init__(self, bucket=settings.AWS_STORAGE_BUCKET_NAME, 
			access_key=None, secret_key=None, acl='public-read', 
			calling_format=settings.AWS_CALLING_FORMAT):
		self.bucket = bucket
		self.acl = acl

		if not access_key and not secret_key:
			 access_key, secret_key = self._get_access_keys()

		self.connection = AWSAuthConnection(access_key, secret_key, 
							calling_format=calling_format)
		self.generator = QueryStringAuthGenerator(access_key, secret_key, 
							calling_format=calling_format, is_secure=False)
		
		self.headers = getattr(settings, AWS_HEADERS, {})

	def _get_access_keys(self):
		access_key = getattr(settings, ACCESS_KEY_NAME, None)
		secret_key = getattr(settings, SECRET_KEY_NAME, None)
		if (access_key or secret_key) and (not access_key or not secret_key):
			access_key = os.environ.get(ACCESS_KEY_NAME)
			secret_key = os.environ.get(SECRET_KEY_NAME)

		if access_key and secret_key:
			# Both were provided, so use them
			return access_key, secret_key

		return None, None

	def _get_connection(self):
		return AWSAuthConnection(*self._get_access_keys())

	def _put_file(self, name, content, extra_headers=None):
		name = _normalize_file_name(name)
		content_type = guess_type(name)[0] or "application/x-octet-stream"		
		self.headers.update({'x-amz-acl': self.acl, 'Content-Type': content_type})
		if extra_headers is not None:
			self.headers.update(extra_headers)
		response = self.connection.put(self.bucket, name, content, self.headers)

	def _open(self, name, mode='rb'):
		name = _normalize_file_name(name)
		remote_file = S3StorageFile(name, self, mode=mode)
		return remote_file

	def _read(self, name, start_range=None, end_range=None):
		name = _normalize_file_name(name)
		if start_range is None:
			headers = {}
		else:
			headers = {'Range': 'bytes=%s-%s' % (start_range, end_range)}
		response = self.connection.get(self.bucket, name, headers)
		headers = response.http_response.msg
		return response.object.data, headers.get('etag', None), headers.get('content-range', None)
		
	def _save(self, name, content, extra_headers=None):
		name = _normalize_file_name(name)
		content.open()
		if hasattr(content, 'chunks'):
			content_str = ''.join(chunk for chunk in content.chunks())
		else:
			content_str = content.read()
		self._put_file(name, content_str, extra_headers)
		cache.set(urlquote(name), time.localtime(), SKIP_CHECKING_IF_FILE_EXISTS_TIMEOUT)
		return name
	
	def delete(self, name):
		name = _normalize_file_name(name)
		self.connection.delete(self.bucket, name)
		cache.delete(urlquote(name))

	def exists(self, name):
		#logging.info("Checking if %s exists" % name)
		name = _normalize_file_name(name)
		if cache.get(urlquote(name)):
			return True
		else:
			response = self.connection._make_request('HEAD', self.bucket, name)
			if response.status != 200:
				return False
			last_modified = response.getheader('Last-Modified')
			last_modified = last_modified and int(mktime(parsedate(last_modified))) or int(0)
			cache.set(urlquote(name), last_modified, SKIP_CHECKING_IF_FILE_EXISTS_TIMEOUT)
			return True
		return False
		
	def getmtime(self, name):
		if cache.get(urlquote(name)):
			return cache.get(urlquote(name))
		response = self.connection._make_request('HEAD', self.bucket, name)
		if response.status != 200:
			return False
		last_modified = response.getheader('Last-Modified')
		last_modified = last_modified and int(mktime(parsedate(last_modified))) or int(0)
		cache.set(urlquote(name), last_modified, SKIP_CHECKING_IF_FILE_EXISTS_TIMEOUT)			
		return last_modified

	def size(self, name):
		name = _normalize_file_name(name)
		response = self.connection.get_info(self.bucket, name)
		content_length = response.getheader('Content-Length')
		return content_length and int(content_length) or 0
	
	def url(self, name):
		name = _normalize_file_name(name)
		return self.generator.make_bare_url(self.bucket, name)

	## UNCOMMENT BELOW IF NECESSARY
	#def get_available_name(self, name):
	#	""" Overwrite existing file with the same name. """
	#	return name


class S3StorageFile(File):
	def __init__(self, name, storage, mode):
		self._name = name
		self._storage = storage
		self._mode = mode
		self._is_dirty = False
		self.file = StringIO()
		self.start_range = 0
	
	@property
	def size(self):
		if not hasattr(self, '_size'):
			self._size = self._storage.size(self._name)
		return self._size

	def read(self, num_bytes=None):		
		if num_bytes is None:
			args = []
			self.start_range = 0
		else:
			args = [self.start_range, self.start_range+num_bytes-1]
		data, etags, content_range = self._storage._read(self._name, *args)
		if content_range is not None:
			current_range, size = content_range.split(' ', 1)[1].split('/', 1)
			start_range, end_range = current_range.split('-', 1)
			self._size, self.start_range = int(size), int(end_range)+1
		self.file = StringIO(data)
		return self.file.getvalue()

	def write(self, content):
		if 'w' not in self._mode:
			raise AttributeError("File was opened for read-only access.")
		self.file = StringIO(content)
		self._is_dirty = True

	def close(self):
		if self._is_dirty:
			self._storage._put_file(self._name, self.file.getvalue())
		self.file.close()
