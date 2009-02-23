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
        post_model = Paste()
        if users.get_current_user():
            post_model.author = users.get_current_user()


        post_expiry = self.request.get('expiry')

        if post_expiry == 'd':
            post_model.expiry = datetime.now()  + timedelta(days=1)
        elif post_expiry == 'm':
            post_model.expiry = datetime.now()  + timedelta(days=1)
        elif post_expiry == 'f':
            post_model.expiry = None

        post_model.content = self.request.get('sendfile')        
        post_model.previous_content = None
        post_model.modified = False
        post_model.modifier = None
        post_model.save()
        self.redirect('/' + str(post_model.key().id()))