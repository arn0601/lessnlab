import hashlib
import boto
import time, base64, hmac, sha, urllib
from django.core.files.storage import default_storage
from django.core.files.base import ContentFile
from django.core.cache import cache
from django.db import models
from django.conf import settings
from boto.s3.connection import S3Connection
from boto.s3.key import Key
from django.http import HttpResponse
from django.utils import simplejson


def getS3Connection():
	return boto.connect_s3(settings.AWS_ACCESS_KEY_ID, settings.AWS_SECRET_ACCESS_KEY)

def handle_upload_file(f):
	h = store_in_s3("test", f, "private")
	return h

def store_in_s3(filename, content, acl):
		conn = getS3Connection()
		b = conn.lookup('lessnlab2')
		#mime = mimetypes.guess_type(content)[0]
		h = hashlib.sha224(str( hash(content))).hexdigest()
		print h
		k = Key(b)
		k.key = h
		#k.set_metadata("Content-Type", mime)
		k.set_contents_from_file(content)
		k.set_acl(acl)
		return h


def getViewableURL(timeout,keyname):
	conn = getS3Connection()
	print "Trying to get:",keyname
	url = conn.generate_url(timeout, 'GET', bucket=settings.AWS_STORAGE_BUCKET_NAME, key=keyname, force_http=True)
	print "URL",url
	return url

def uploadData(request):
    # Collect information on the file from the GET parameters of the request:
    object_name = request.GET.get('s3_object_name')
    mime_type = request.GET.get('s3_object_type')
 
    # Set the expiry time of the signature (in seconds) and declare the permissions of the file to be uploaded
    expires = int(time.time()+40)
    amz_headers = "x-amz-acl:private"
 
    # Generate the PUT request that JavaScript will use:
    put_request = "PUT\n\n%s\n%d\n%s\n/%s/%s" % (mime_type, expires, amz_headers, settings.AWS_STORAGE_BUCKET_NAME, object_name)
  
    # Generate the signature with which the request can be signed:
    signature = base64.encodestring(hmac.new(settings.AWS_SECRET_ACCESS_KEY, put_request, sha).digest())
    # Remove surrounding whitespace and quote special characters:
    signature = urllib.quote_plus(signature.strip())

    # Build the URL of the file in anticipation of its imminent upload:
    #url = json_helpers.getViewableURL(30,object_name);
    url = 'https://%s.s3.amazonaws.com/%s' % (settings.AWS_STORAGE_BUCKET_NAME, object_name)
 
    # Return the signed request and the anticipated URL back to the browser in JSON format:
    return HttpResponse(simplejson.dumps({
            'signed_request': '%s?AWSAccessKeyId=%s&Expires=%d&Signature=%s' % (url, settings.AWS_ACCESS_KEY_ID, expires, signature),
            'url': url
        }))

