import logging

from google.appengine.ext import webapp

from isimplebin_utils import *

class View(webapp.RequestHandler):
    def get(self, paste_id):                
        paste = model.get_paste(paste_id)
        self.response.headers['Content-Type'] = 'text/plain'
        self.response.headers['Content-Disposition'] =  'attachment; filename=' + paste_id + '.txt'
        self.response.out.write(paste.previous_content)