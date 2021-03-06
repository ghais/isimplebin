import cgi
import logging
from google.appengine.api import users
from google.appengine.ext import webapp
from google.appengine.ext.webapp.util import run_wsgi_app
from google.appengine.ext.webapp import template
from datetime import datetime
from datetime import timedelta
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
        post_model.old_content = None
        post_model.modified = False
        post_model.modifier = None
        post_model.save()
        self.redirect('/' + str(post_model.key().id()))

        
class Upload(webapp.RequestHandler):
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

        path = os.path.join(os.path.dirname(__file__), 'html/upload.html')
        self.response.out.write(template.render(path, template_values))
        
        
class Update(webapp.RequestHandler):
    def post(self):
        db_id = self.request.uri.split("/")[-1]
        view = PostModel.get_by_id(int(self.request.uri.split("/")[-1]))
        content = self.request.get('content')
        view.old_content = view.content
        view.content = content
        view.modified = True
        if users.get_current_user():
            view.modifier = users.get_current_user()
        else:
            view.modifier = None
        view.save()
        self.redirect('/' + db_id)
        
class Upload_Action(webapp.RequestHandler):
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

        post_model.content = self.request.get('sendfile')        
        post_model.old_content = None
        post_model.modified = False
        post_model.modifier = None
        post_model.save()
        self.redirect('/' + str(post_model.key().id()))
        

class Post(webapp.RequestHandler):
    def get(self):
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
            lines = view.content.splitlines()
        else:
            code = ""
            lines = []
        highlighted = []
        views = []
        for i in xrange(len(lines)):
            views.append({'content':lines[i] , 'i' : 'li'})
            if lines[i].find("@@") != -1:
                highlighted.append(i + 1)
        code = code.replace("@@", "")
        line = highlight(code, PythonLexer(), CodeHtmlFormatter(hl_lines=highlighted))

        template_values = {
            'posts' : posts,
            'lines' : lines,
            'url' : url,
            'url_linktext' : url_linktext,
            'line': line,
            'id' : self.request.uri.split("/")[-1],
            'view' : view,
            'expiry': view.expiry if view else None,
            'download_link' : "download/" + str(view.key().id()) if view else ''
        }
        if view :
            path = os.path.join(os.path.dirname(__file__), 'html/view.html')
        else :
            path = os.path.join(os.path.dirname(__file__), 'html/404.html')
            self.error(404)

        self.response.out.write(template.render(path, template_values))

class Download(webapp.RequestHandler):
    def get(self):
        db_id = self.request.get('id')
        v = self.request.get('v')

        self.response.out.write(v)
        self.response.headers['Content-Type'] = 'text/plain'
        self.response.headers['Content-Disposition'] =  'attachment; filename=' + db_id + '.txt'
        view = PostModel.get_by_id(int(db_id))
        if v == 'c':
            self.response.out.write(view.content)
        elif v == 'o':
            self.response.out.write(view.old_content)
        elif v == 'd':
            #self.redirect('/diff/' + str(view.key().id()))
            self.redirect('/' + str(view.key().id()))
        else:
            self.response.out.write('foooooooooooo you')    


application = webapp.WSGIApplication(
    [('/', MainPage),
     ('/download.*?.*', Download),
     ('/submit', Form),
     ('/update/.*', Update),
     ('/upload', Upload),
     ('/uploadaction', Upload_Action),
     ('/.*', Post )],
    debug=True)

def main():
    logging.getLogger().setLevel(logging.DEBUG)
    run_wsgi_app(application)
    logging.debug("Hello world")

if __name__ == "__main__":
    main()
