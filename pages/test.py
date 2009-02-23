import logging
import os
from datetime import datetime

from google.appengine.ext import webapp
from google.appengine.ext.webapp import template

from isimplebin_utils import *



class Foo(webapp.RequestHandler):
    def get(self):
        template_values = {}
        path = os.path.join(os.path.dirname(__file__), 'html/base.html')        
        self.response.out.write(template.render(path, template_values))