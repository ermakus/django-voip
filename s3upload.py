#!/bin/python
import mimetypes
import os.path
import sys
from backends import S3 # Get this from Amazon

from localsettings import *

def update_s3():
    print "Connecting to S3.."
    conn = S3.AWSAuthConnection(AWS_ACCESS_KEY_ID, AWS_SECRET_ACCESS_KEY)
    filename = os.path.normpath(sys.argv[1])
    if not os.path.isfile(filename):
        print "Invalid file: %s" % filename
        return

    print "Uploading %s" % filename
    filedata = open(filename, 'rb').read()
    content_type = mimetypes.guess_type(filename)[0]
    if not content_type:
        content_type = 'text/plain'
    conn.put(AWS_STORAGE_BUCKET_NAME, filename, S3.S3Object(filedata),{'x-amz-acl': 'public-read', 'Content-Type': content_type})

if __name__ == "__main__":
    update_s3()
