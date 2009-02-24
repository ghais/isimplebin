import logging

from google.appengine.ext import webapp
from google.appengine.ext.webapp.util import run_wsgi_app

import pages
import pages.index
import pages.paste
import pages.view
import pages.update
import pages.upload
import pages.download
import pages.diff
import pages.original
import pages.personal
import pages.test


application = webapp.WSGIApplication(
    [('/', pages.index.MainPage),
     ('/foo', pages.test.Foo),    
     ('/submit', pages.paste.Paste),
     ('/update/([a-zA-Z0-9_-]+)', pages.update.Update),
     ('/upload', pages.upload.Upload),
     ('/uploadaction', pages.upload.UploadAction),
     ('/download/([a-zA-Z0-9_-]+)', pages.download.Download),
     ('/original/([a-zA-Z0-9_-]+)', pages.original.Download),
     ('/diff/([a-zA-Z0-9_-]+)', pages.diff.Diff),
     ('/mypastes', pages.personal.MyPastes),
     ('/([a-zA-Z0-9_-]+)', pages.view.ViewPaste),
     ],
    debug=True)

def main():
    logging.getLogger().setLevel(logging.DEBUG)
    run_wsgi_app(application)

if __name__ == "__main__":
    main()
