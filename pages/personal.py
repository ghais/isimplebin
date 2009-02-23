import os
import logging

from google.appengine.ext import webapp
from google.appengine.api import users
from google.appengine.ext.webapp import template
from google.appengine.ext import webapp

from isimplebin_utils import *
from isimplebin_utils import login_required
class MyPastes(webapp.RequestHandler):
    def get(self):
        self._get_pastes()
        
        
    @login_required
    def _get_pastes(self):
        pastes = Paste.gql("WHERE author = :author ORDER BY date DESC",
                           author = users.get_current_user())
