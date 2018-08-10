import os
from flask import Blueprint,request,render_template,flash,redirect,url_for
from flask import session,g
from werkzeug.security import generate_password_hash,check_password_hash
from user.form import LoginForm,RegisterForm
from user.models import db
from user.models import User
from common_function import random_Name,after_login

user = Blueprint("user",__name__)

@user.route('/login/',methods=["GET","POST"])
def login():
    if request.method == "GET":
        form = LoginForm()
        return render_template('user/login.html', form=form)

    else:
        form = LoginForm(formdata=request.form)
        # 验证是否符合表单校验
        if form.validate():
            password = form.password.data
            # 查找该用户
            user = User.query.filter_by(username=form.username.data).first()
            if check_password_hash(user.password,password) is False:
                flash("用户名或密码错误")
                return render_template('user/login.html',form=form)
            else:
                flash("登录成功")
                session['user'] = user.to_dict()
                return redirect(url_for("index"))
        else:
            # print(form.errors)
            return render_template('user/login.html', form=form)

@user.route('/register/',methods=["GET","POST"])
def register():
    if request.method == "GET":
        # data = jsonify("please register")
        # print(type(data))
        form = RegisterForm()
        return render_template('user/register.html',form=form)
    elif request.method == "POST":
        form = RegisterForm(formdata=request.form)
        # 判断是否验证成功
        if form.validate():
            isexist = User.query.filter_by(username=form.username.data).first()
            if isexist:
                flash(message="用户已存在")
                return redirect(url_for('user.register'))
            else:
                user = User(username=form.username.data,
                            password=generate_password_hash(form.password.data))
            # 将验证通过的用户保存至数据库
                db.session.add(user)
                db.session.commit()
                flash("注册成功,赶紧登录吧")
                return redirect(url_for('user.login'))
        else:
            # 消息闪现，是一个列表
            flash("注册失败")
            return render_template('user/register.html',form=form)



@user.route("/uploads/icon/",methods=["GET","POST"])
@after_login
def uploads():
    if request.method == "GET":
        return render_template('user/uploads.html')
    elif request.method == "POST":
        if session.get("user"):
            img_url = None
            # 获取上传的图片
            icon = request.files.get("icon")
            if icon:
                suffix = os.path.splitext(icon.filename)[-1]
                # 新名字
                newName = random_Name(suffix)
                from myblog.index import photo
                photo.save(icon,name=newName)
                img_url = photo.url(newName)
                # 获得用户对象保存头像url
                user = User.query.get(session["user"]["id"])
                user.icon = img_url
                db.session.commit()
                # 提示上传成功
                flash("上传成功")
                # 调用并执行上下文函数
                user_info()
                return redirect(url_for("index"))
            else:
                error = "您还没有选择图片，选择之后再上传"
                return render_template('user/uploads.html',error=error)
        else:
            # 未登录跳转到登录页面
            return redirect(url_for("user.login"))

# 应用上下文对象
@user.app_context_processor
def user_info():
    if session.get("user"):
        username = session["user"]["username"]
        # 重新刷新返回的字典对象
        user = User.query.filter_by(username=username).first()
        user_dict = user.to_dict()
        session["user"] = user_dict
        return session.get("user")
    else:
        return {}

@user.route("/logout/")
@after_login
def logout():
    session.pop("user")
    return redirect(url_for("index"))