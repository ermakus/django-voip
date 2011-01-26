# coding=UTF-8
from django.template import Library, Node, Template, TemplateSyntaxError, \
                            Variable
from django.utils.translation import ugettext as _
from userprofile.models import Avatar, AVATAR_SIZES, S3BackendNotFound, \
        DEFAULT_AVATAR_SIZE, DEFAULT_AVATAR, DEFAULT_AVATAR_FOR_INACTIVES_USER, \
        SAVE_IMG_PARAMS
from django.contrib.auth.models import User
from django.core.files.base import ContentFile
import urllib
from cStringIO import StringIO
from django.conf import settings
try:
    from PIL import Image
except ImportError:
    import Image

# from PythonMagick import Image
#from utils.TuxieMagick import Image
import os
import urlparse
import time
from django.core.files.storage import default_storage
if hasattr(settings, "AWS_SECRET_ACCESS_KEY"):
    try:
        from backends.S3Storage import S3Storage
        storage = S3Storage()
    except ImportError:
        raise S3BackendNotFound
else:
    storage = default_storage

register = Library()

class ResizedThumbnailNode(Node):
    def __init__(self, size, username=None):
        try:
            self.size = int(size)
        except:
            self.size = Variable(size)

        if username:
            self.user = Variable(username)
        else:
            self.user = Variable("user")

    def render(self, context):
        # If size is not an int, then it's a Variable, so try to resolve it.
        size = self.size
        if not isinstance(size, int):
            size = int(self.size.resolve(context))

        if not size in AVATAR_SIZES:
            return ''

        try:
            user = self.user.resolve(context)
            if DEFAULT_AVATAR_FOR_INACTIVES_USER and not user.is_active:
                raise
            avatar = Avatar.objects.get(user=user, valid=True).image
            if hasattr(settings, "AWS_SECRET_ACCESS_KEY"):
                avatar_path = avatar.name
            else:
                avatar_path = avatar.path

            if not storage.exists(avatar_path):
                raise
            base, filename = os.path.split(avatar_path)
            name, extension = os.path.splitext(filename)
            filename = os.path.join(base, "%s.%s%s" % (name, size, extension))
            base_url = avatar.url

        except:
            avatar_path = DEFAULT_AVATAR
            avatar = open(avatar_path)
            base, filename = os.path.split(avatar_path)
            name, extension = os.path.splitext(filename)
            filename = os.path.join(base, "%s.%s%s" % (name, size, extension))
            base_url = filename.replace(settings.MEDIA_ROOT, settings.MEDIA_URL)

        url_tuple = urlparse.urlparse(base_url)
        url = urlparse.urljoin(urllib.unquote(urlparse.urlunparse(url_tuple)), "%s.%s%s" % (name, size, extension))

        if not storage.exists(filename):
            thumb = Image.open(ContentFile(avatar.read()))
            img_format = thumb.format
            if not getattr(settings, 'CAN_ENLARGE_AVATAR', True ) or (thumb.size[0] > size or thumb.size[1] > size or not hasattr(thumb, 'resize')):
                thumb.thumbnail((size, size), Image.ANTIALIAS)
            else:
                thumb = thumb.resize((size, size), Image.BICUBIC)
            f = StringIO()
            try:
                thumb.save(f, img_format, **SAVE_IMG_PARAMS.get(img_format, {}))
            except:
                thumb.save(f, img_format)
            f.seek(0)
            storage.save(filename, ContentFile(f.read()))

        return url

@register.tag('avatar')
def Thumbnail(parser, token):
    bits = token.contents.split()
    username = None
    if len(bits) > 3:
        raise TemplateSyntaxError, _(u"You have to provide only the size as \
            an integer (both sides will be equal) and optionally, the \
            username.")
    elif len(bits) == 3:
        username = bits[2]
    elif len(bits) < 2:
        bits.append(str(DEFAULT_AVATAR_SIZE))
    return ResizedThumbnailNode(bits[1], username)
