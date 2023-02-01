import random
import string
from thousand_sails_race.models import EmailCaptchaModel, UserModel
from flask import Blueprint, render_template, request, jsonify, redirect, url_for, session, flash
from thousand_sails_race.extends import mail, db
from flask_mail import Message
from thousand_sails_race.forms import RegisterForm, LoginForm
from werkzeug.security import generate_password_hash, check_password_hash

bp = Blueprint("auth", __name__, url_prefix="/auth")


@bp.route("/login", methods=['GET', 'POST'])
def login():
    if request.method == 'GET':
        form = LoginForm()
        return render_template("login.html", form=form)
    else:
        form = LoginForm(request.form)
        if form.validate():
            email = form.email.data
            password = form.password.data
            user = UserModel.query.filter_by(email=email).first()
            if not user:
                print("邮箱在数据库中不存在")
                return redirect(url_for("auth.login"))
            # if check_password_hash(user.password, password):
            if check_password_hash(user.password, password):
                # cookie: 一般用来存放登录授权
                # flask中的 session 是经过加密后存储在 cookie
                flash("welcome on")
                session['username'] = user.username
                return redirect("/")
            else:
                print("密码错误")
                return redirect(url_for("auth.login"))
        else:
            print(form.errors)
            return redirect(url_for("auth.login"))


# GET 是从服务器获取数据
# POST：将客户端的数据提交给服务器
@bp.route("/register", methods=['GET', 'POST'])
def register():
    if request.method == 'GET':
        form = RegisterForm()
        return render_template("register.html", form=form)
    else:
        # 验证用户提交的邮箱和验证码是否对应且正确
        # 表单验证： flask—wtf：wtforms
        # 返回一个对象
        form = RegisterForm(request.form)
        if form.validate():
            email = form.email.data
            username = form.username.data
            password = form.password.data
            user = UserModel(email=email, username=username, password=generate_password_hash(password))
            db.session.add(user)
            db.session.commit()
            # return redirect("/auth/login")
            return redirect(url_for("auth.login"))

        else:
            print(form.errors)
            return redirect(url_for("auth.register"))