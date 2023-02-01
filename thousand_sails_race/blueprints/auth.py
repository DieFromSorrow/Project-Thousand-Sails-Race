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
    form = LoginForm()
    if form.validate_on_submit():
        email = form.email.data
        password = form.password.data
        print(password)
        user = UserModel.query.filter_by(email=email).first()

        if check_password_hash(user.password, password):
            # cookie: 一般用来存放登录授权
            # flask中的 session 是经过加密后存储在 cookie
            flash("welcome on")
            session['username'] = user.username
            return redirect("/")
        else:
            flash("密码错误")
    return render_template('login.html', form=form)


# GET 是从服务器获取数据
# POST：将客户端的数据提交给服务器
@bp.route("/register", methods=['GET', 'POST'])
def register():
    form = RegisterForm()
    if form.validate_on_submit():
        # 验证用户提交的邮箱和验证码是否对应且正确
        # 表单验证： flask—wtf：wtforms
        # 返回一个对象
        email = form.email.data
        username = form.username.data
        password = form.password.data
        user = UserModel(email=email, username=username, password=generate_password_hash(password))
        db.session.add(user)
        db.session.commit()
        # return redirect("/auth/login")
        return redirect(url_for("auth.login"))
    return render_template("register.html", form=form)


@bp.route('/logout')
def logout():
    if 'username' in session:
        session.pop('username')
        flash('成功登出')
    return redirect('/')
