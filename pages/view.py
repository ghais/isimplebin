import os
import logging

from google.appengine.ext import webapp
from google.appengine.api import users
from google.appengine.ext.webapp import template	

from isimplebin_utils import *
from pygments import highlight
from pygments.lexers import *


class ViewPaste(webapp.RequestHandler):
    def get(self, paste_id):
        pastes = model.get_recent_pastes()
        paste = model.get_paste(paste_id)
        
        original = model.get_original(paste_id)
        
        if users.get_current_user():
            url = users.create_logout_url(self.request.uri)
            url_linktext = 'Logout'
        else:
            url = users.create_login_url(self.request.uri)
            url_linktext = 'Login'
        
                        
        if paste:
            code = paste.content
            lines = paste.content.splitlines()
        else:
            code = ""
            lines = []
        highlighted = []
        views = []
        
        
        
        for i in xrange(len(lines)):
            if lines[i].find("@@") != -1:
                highlighted.append(i + 1)
        code = code.replace("@@", "")

        try:
            if paste.lexer == "none":
                lexer = None
            else:
                lexer = get_lexer_by_name(paste.lexer)
        except:
            lexer = PythonLexer()

        if lexer:
            code = highlight(code, lexer, CodeHtmlFormatter(hl_lines=highlighted))
        else:
            code = '<pre>' + code + '</pre>'
        
        template_values = {
            'pastes' : pastes,
            'paste' : paste,
            'lines' : lines,
            'url' : url,
            'url_linktext' : url_linktext,
            'code' : code,
            'download_link' : "download/" + str(paste.key().id()) if paste else '',
            'original' : original,
            'lexer' : paste.lexer.lower(),
        }
        
        if paste:
            path = os.path.join(os.path.dirname(__file__), 'html/view.html')
        else :
            path = os.path.join(os.path.dirname(__file__), 'html/404.html')
            self.error(404)

        self.response.out.write(template.render(path, template_values))
