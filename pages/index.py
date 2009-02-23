import os
import logging

from google.appengine.ext import webapp
from google.appengine.api import users
from google.appengine.ext.webapp import template

from isimplebin_utils import *

class MainPage(webapp.RequestHandler):
    def get(self):
        pastes = model.get_recent_pastes()

        if users.get_current_user():
            url = users.create_logout_url(self.request.uri)
            url_linktext = "Logout"
        else:
            url = users.create_login_url(self.request.uri)
            url_linktext = "Login"

        template_values = {
            'pastes' : pastes,
            'url' : url,
            'url_linktext' : url_linktext
        }

        path = os.path.join(os.path.dirname(__file__), 'html/index.html')
        self.response.out.write(template.render(path, template_values))
