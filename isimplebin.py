import cgi
import logging
from google.appengine.api import users
from google.appengine.ext import webapp
from google.appengine.ext.webapp.util import run_wsgi_app
from google.appengine.ext.webapp import template
from datetime import datetime
from datetime import timedelta
import uuid
import os
from pygments import highlight
from pygments.lexers import PythonLexer
from formater import CodeHtmlFormatter

from date_model import PostModel


class MainPage(webapp.RequestHandler):
    def get(self):
        posts_query = PostModel().all().order('-date')
        posts = posts_query.fetch(10)   

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

        path = os.path.join(os.path.dirname(__file__), 'html/index.html')
        self.response.out.write(template.render(path, template_values))

class Form(webapp.RequestHandler):
    def post(self):
        post_model = PostModel()
        if users.get_current_user():
            post_model.author = users.get_current_user()

            
        post_expiry = self.request.get('expiry')
        
        if post_expiry == 'd':
            post_model.expiry = datetime.now()  + timedelta(days=1)
        elif post_expiry == 'm':
            post_model.expiry = datetime.now()  + timedelta(days=1)
        elif post_expiry == 'f':
            post_model.expiry = None
        
        post_model.content = self.request.get('content')        
        post_model.modified = False
        post_model.modifier = None
        post_model.save()
        self.redirect('/' + str(post_model.key().id()))

class Update(webapp.RequestHandler):
    def post(self):
        db_id = self.request.uri.split("/")[-1]
        view = PostModel.get_by_id(int(self.request.uri.split("/")[-1]))
        content = self.request.get('content')
        view.content = content
        view.modified = True
        if users.get_current_user():
            view.modifier = users.get_current_user()
        else:
            view.modifier = None
        view.save()
        self.redirect('/' + db_id)

class Post(webapp.RequestHandler):
    def get(self):
        logging.debug("Hello world")
        posts_query = PostModel().all().order('-date')
        posts = posts_query.fetch(10)
        try:
            view = PostModel.get_by_id(int(self.request.uri.split("/")[-1]))
        except ValueError:
            view = None

        if users.get_current_user():
            url = users.create_logout_url(self.request.uri)
            url_linktext = 'Logout'
        else:
            url = users.create_login_url(self.request.uri)
            url_linktext = 'Login'

        if view:
            code = view.content
            lines = view.content.split("\n")
        else:
            code = ""
            lines = []
        highlighted = []
        views = []
        for i in xrange(len(lines)):
            views.append({'content':lines[i] , 'i' : 'li'})
            if lines[i].find("@@") != -1:
                highlighted.append(i + 1)
        line = highlight(code, PythonLexer(), CodeHtmlFormatter(hl_lines=highlighted))

        template_values = {
            'posts' : posts,
            'lines' : views,
            'url' : url,
            'url_linktext' : url_linktext,
            'line': line.replace("@@", ""),
            'id' : self.request.uri.split("/")[-1],
            'view' : view,
            'expiry': view.expiry,
        }
        if view :
            path = os.path.join(os.path.dirname(__file__), 'html/view.html')
        else :
            path = os.path.join(os.path.dirname(__file__), 'html/404.html')
            
        self.response.out.write(template.render(path, template_values))

application = webapp.WSGIApplication(
    [('/', MainPage),
     ('/submit', Form),
     ('/update/.*', Update),
     ('/.*', Post )],
    debug=True)

def main():
    logging.getLogger().setLevel(logging.DEBUG)
    run_wsgi_app(application)
    logging.debug("Hello world")

if __name__ == "__main__":
    main()
