
from flask import session, redirect, url_for,flash
from functools import wraps


def login_verification(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        if 'login' not in session:
            flash('请先登录')
            return redirect(url_for('auth.auth', action='login'))
        return func(*args, **kwargs)

    return wrapper
