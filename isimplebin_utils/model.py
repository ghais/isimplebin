import logging

from google.appengine.ext import db
from google.appengine.api import users
from datetime import datetime
from tokens import *


logging.basicConfig(level=logging.DEBUG)

class PasteUser(db.Model):
    user = db.UserProperty(auto_current_user_add=True)


class Paste(db.Model):
    paste_key = db.StringProperty()
    
    author = db.ReferenceProperty(PasteUser, collection_name="author_reference")
    
    title = db.StringProperty()
    atom_feed = db.TextProperty()    
    ip_address = db.StringProperty()
    tags = db.StringListProperty()
    content = db.TextProperty()
    lexer = db.StringProperty()
    
    date = db.DateTimeProperty(auto_now_add=True)
    expiry = db.DateTimeProperty()
    
    previous = db.SelfReference()
    
    is_original = db.BooleanProperty()
        
    
    def __str__(self):
        result = ""
        result += "key: " + self.paste_key + "\n"
        if self.author.user:
            result += "author: " + self.author.user.nickname() + "\n" 
        else:
            result += "author: Anonymous\n" 
        result += "title: " +  str(self.title) + "\n"
        result += "content: " + self.content  + "\n"
        result += "date: " + str(self.date) + "\n"
        result += "exipiry: " + str(self.expiry) + "\n"
        result += "is original: " + str(self.is_original) + "\n"
        result += "previous: " + str(self.previous)
        return result
    

        
def insert(expiry, content, lexer = None, title=None, tags = [], ip_address=None):
    paste = Paste()
    paste_key = make_token()
    while Paste.all().filter("paste_key=", paste_key).fetch(1) != []:
        paste_key = make_token()
        
    paste.paste_key = paste_key
    
    user = PasteUser()
    user.save()
    paste.author = user
    paste.title = title
    paste.tags = tags
    paste.expiry = expiry
    paste.ip_address = ip_address
    paste.content = content
    
    paste.previous = None
    
    paste.is_original = True
    paste.lexer = lexer.lower()
    paste.save()
    return paste
    
    
    
def get_recent_pastes(n = 10):
    pastes = Paste.all().filter("is_original = ", True).order("-date")
    return pastes.fetch(n)


def update(paste_id, content, lexer = None, tags = [], ip_address = None):
    pastes = Paste.all().filter("paste_key =", paste_id).order('-date')    
    last_edit = pastes.get()
    
    if not last_edit:
        raise KeyError()
    
    
    paste = Paste()
    paste.paste_key = last_edit.paste_key
    
    user = PasteUser()
    user.save()
    
    paste.author = user
    
    paste.title = last_edit.title
    paste.tags = tags
    paste.ip_address = ip_address
    paste.content = content
    paste.previous = last_edit
    paste.lexer = lexer.lower()
    paste.save()        
    
    return paste
    
    
def get_paste(paste_id, revision = 1):
    
    pastes = Paste.all().filter("paste_key =", paste_id).order("-date")
    return pastes.fetch(revision)[revision - 1]

def get_original(paste_id):
    pastes = Paste.all().filter("paste_key =", paste_id).filter(
        "is_original = ", True).order("-date")
    return pastes.get()
    
