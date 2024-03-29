import os
import urllib
import webapp2

from google.appengine.api import images # import images to manipulate images
from google.appengine.ext import blobstore
from google.appengine.ext.webapp import blobstore_handlers

class MainHandler(webapp2.RequestHandler):
	def get(self):
		upload_url = blobstore.create_upload_url('/upload')
		self.response.out.write('<html><body>')
		self.response.out.write('<form action="%s" method="POST" enctype="multipart/form-data">' %upload_url)
		self.response.out.write("""Upload File <input type="file" name="file"><br/> <input type="submit" name="submit" value="Submit"></form></body></html>""")

class UploadHandler(blobstore_handlers.BlobstoreUploadHandler):
	def post(self):
		upload_files = self.get_uploads('file') 
		blob_info = upload_files[0]
		self.redirect('serve/%s' % blob_info.key()) # serving image with blob key

# Here is the handler to serving the image
class ServeHandler(blobstore_handlers.BlobstoreDownloadHandler):
	def get(self, resource):
		resource = str(urllib.unquote(resource))
		blob_info = blobstore.BlobInfo.get(resource)

		# Resizing Part
		img = images.Image(blob_key=resource)
		img.resize(width=1000)
		img.crop(left_x=0.3, top_y=0.3, right_x=0.8, bottom_y=0.7)
		img.rotate(90)
		img.im_feeling_lucky()
		image = img.execute_transforms(output_encoding=images.JPEG)

		self.response.headers['Content-Type'] = 'image/jpeg'
		self.response.out.write(image)

		return

# app
app = webapp2.WSGIApplication([('/', MainHandler),
	                       ('/upload', UploadHandler),
			       ('/serve/([^/]+)?',ServeHandler)],
			       debug=True)

