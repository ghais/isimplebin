import os
import logging

from google.appengine.ext import webapp
from google.appengine.api import users
from google.appengine.ext.webapp import template

from isimplebin_utils import *

class Update(webapp.RequestHandler):
    def post(self, paste_id):
        model.update(paste_id, self.request.get('content'))
        self.redirect('/' + paste_id)