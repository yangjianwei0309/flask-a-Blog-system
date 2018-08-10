import string
import functools
import random
from flask import g,session,request,redirect,url_for

def random_Name(suffix,length=32):
    strings = string.ascii_letters + "123456789"
    name = "".join(random.choice(strings) for i in range(length))+suffix
    return name

# 在请求之前的预处理装饰器
def before_request(func):
    def inner(*args,**kwargs):
        if session.get("user"):
            g.username = session["user"]["username"]
            g.icon = session["user"]["icon"]
            return func(*args,**kwargs)
    return inner

def after_login(func):
    @functools.wraps(func)
    def inner(*args,**kwargs):
        if session.get("user"):
            return func(*args,**kwargs)
        else:
            return redirect(url_for("user.login"))
    return inner

