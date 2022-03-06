from functools import wraps
from flask import session, redirect

def login_required(view):
    @wraps(view)
    def inner(*args, **kwargs):
        if 'user_id' not in session:
            return redirect('/logout')
        return view(*args, **kwargs)
    return inner