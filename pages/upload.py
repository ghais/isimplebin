import os
import logging
from datetime import datetime
from datetime import timedelta

from google.appengine.ext import webapp
from google.appengine.api import users
from google.appengine.ext.webapp import template

from isimplebin_utils import *

class Upload(webapp.RequestHandler):
    def get(self):
        posts = model.get_recent_pastes()

        if users.get_current_user():
            url = users.create_logout_url(self.request.uri)
            url_linktext = "Logout"
        else:
            url = users.create_login_url(self.request.uri)
            url_linktext = "Login"

        template_values = {
            'posts' : posts,
            'url' : url,
            'url_linktext' : url_linktext
        }

        path = os.path.join(os.path.dirname(__file__), 'html/upload.html')
        self.response.out.write(template.render(path, template_values))
        
        
class UploadAction(webapp.RequestHandler):
    def post(self):


        expiry = self.request.get('expiry')
        lexer = self.request.get('lexer')
        
        if expiry == 'd':
            expiry = datetime.now()  + timedelta(days=1)
        elif expiry == 'm':
            expiry = datetime.now()  + timedelta(days=1)
        elif post_expiry == 'f':
            expiry = None

        content = self.request.get('sendfile')        
        
        lexer = lexer.lower()
        paste = model.insert(expiry, content, lexer)
        self.redirect('/' + paste.paste_key)