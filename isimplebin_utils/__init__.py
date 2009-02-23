from model import get_recent_pastes
from model import Paste

from tokens import make_token
from format import CodeHtmlFormatter
from google.appengine.api import users



def login_required(func):
    def _wrapper(request, *args, **kw):
        user = users.get_current_user()
        if user:
            return func(request, *args, **kw)
        else:
            return request.redirect(users.create_login_url(request.request.uri))

    return _wrapper

