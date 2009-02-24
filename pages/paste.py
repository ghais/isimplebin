from datetime import datetime
from datetime import timedelta

from isimplebin_utils import model
from google.appengine.ext import webapp


class Paste(webapp.RequestHandler):
    def post(self):
        expiry = self.request.get('expiry')
        
        if expiry == 'd':
            expiry = datetime.now()  + timedelta(days=1)
        elif expiry == 'm':
            expiry = datetime.now()  + timedelta(days=30)
        elif expiry == 'f':
            expiry = None

        content = self.request.get('content') 
        lexer = self.request.get('lexer')
        assert(lexer)
        paste = model.insert(expiry, content, lexer)
        self.redirect('/' + str(paste.paste_key))