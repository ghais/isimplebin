import cgi
from google.appengine.api import users
from google.appengine.ext import webapp
from google.appengine.ext.webapp.util import run_wsgi_app
from google.appengine.ext.webapp import template
from datetime import datetime
from datetime import timedelta
import os

from date_model import PostModel

class MainPage(webapp.RequestHandler):
    def get(self):
        if users.get_current_user():
            url = users.create_logout_url(self.request.uri)
            url_linktext = 'Logout'
        else:
            url = users.create_login_url(self.request.uri)
            url_linktext = 'Login'
        if users.is_current_user_admin():
            self.response.out.write("Cleaning up")
            posts_query = PostModel.gql("WHERE expiry > :1", datetime.now())
            for query in posts_query:
                query.delete()
        else:
            self.response.out.write("You are not admin")

            

            
def main():
    application = webapp.WSGIApplication([('/.*',MainPage)])
    run_wsgi_app(application)

        

if __name__ == "__main__":
    main()
