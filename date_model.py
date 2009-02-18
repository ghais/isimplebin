from google.appengine.ext import db
class PostModel(db.Model):
    author = db.UserProperty()
    content = db.TextProperty()
    old_content = db.TextProperty()
    date = db.DateTimeProperty(auto_now_add=True)
    modified = db.BooleanProperty()
    modifier = db.UserProperty()
    expiry = db.DateTimeProperty()