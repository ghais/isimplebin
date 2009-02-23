import logging

from google.appengine.ext import webapp


class Diff(webapp.RequestHandler):
    def get(self, paste_id):
        self.redirect('/' + paste_id)