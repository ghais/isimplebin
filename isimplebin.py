import cgi

from google.appengine.api import users
from google.appengine.ext import webapp
from google.appengine.ext.webapp.util import run_wsgi_app
from google.appengine.ext import db
from google.appengine.ext.webapp import template
from datetime import datetime
from datetime import timedelta
import uuid
import os
from pygments import highlight
from pygments.lexers import PythonLexer
from pygments.formatters import HtmlFormatter


class CodeHtmlFormatter(HtmlFormatter):

    def wrap(self, source, outfile):
        return self._wrap_code(self._wrap_div(self._wrap_pre(source)))

    def _wrap_code(self, source):
        yield 0, '<ol class="highlight">' 
        for i, t in source:
            if i == 1:
                # it's a line of formatted code
                t = "<li>" + t + "</li>"
            yield i, t
        yield 0, '</ol>'
        
    def _wrap_div(self, inner):
        yield 0, ('<div' + (self.cssclass and ' class="%s"' % self.cssclass)
                  + (self.cssstyles and ' style="%s"' % self.cssstyles) + '>')
        for tup in inner:
            yield tup
        yield 0, '</div>\n'

    def _wrap_pre(self, inner):
        yield 0, ('<pre'
                  + (self.prestyles and ' style="%s"' % self.prestyles) + '>')
        for tup in inner:
            yield tup
        yield 0, '</pre>'


class PostModel(db.Model):
    author = db.UserProperty()
    content = db.TextProperty()
    date = db.DateTimeProperty(auto_now_add=True)


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

        path = os.path.join(os.path.dirname(__file__), 'index.html')
        self.response.out.write(template.render(path, template_values))

class Form(webapp.RequestHandler):
    def post(self):
        post_model = PostModel()
        if users.get_current_user():
            post_model.author = users.get_current_user()

        post_model.content = self.request.get('content')
        post_model.save()
        self.redirect('/' + str(post_model.key().id()))

class Update(webapp.RequestHandler):
    def post(self):
        db_id = self.request.uri.split("/")[-1]
        view = PostModel.get_by_id(int(self.request.uri.split("/")[-1]))
        content = self.request.get('content')        
        view.content = content
        view.save()
        self.redirect('/' + db_id)

class Post(webapp.RequestHandler):
    def get(self):
        posts_query = PostModel().all().order('-date')
        posts = posts_query.fetch(10)   
        view = PostModel.get_by_id(int(self.request.uri.split("/")[-1]))

        if users.get_current_user():
            url = users.create_logout_url(self.request.uri)
            url_linktext = 'Logout'
        else:
            url = users.create_login_url(self.request.uri)
            url_linktext = 'Login'


        lines = view.content.split("\n")
        views = []
        highlighted = []
        for i in xrange(len(lines)):
            views.append({'content':lines[i] , 'i' : 'li'})
            if lines[i].find("@@") != -1:
                highlighted.append(i + 1)
        line = highlight(view.content, PythonLexer(), CodeHtmlFormatter(hl_lines=highlighted))

        template_values = {
            'posts' : posts,
            'lines' : views,
            'url' : url,
            'url_linktext' : url_linktext,
            'line': line.replace("@@", "  "),
            'id' : self.request.uri.split("/")[-1],
        }

        path = os.path.join(os.path.dirname(__file__), 'view.html')
        self.response.out.write(template.render(path, template_values))

application = webapp.WSGIApplication(
    [('/', MainPage),
     ('/submit', Form),
     ('/update/.*', Update),
     ('/.*', Post )],
    debug=True)

def main():
    run_wsgi_app(application)

if __name__ == "__main__":
    main()
