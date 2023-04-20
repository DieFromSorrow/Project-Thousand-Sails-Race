from thousand_sails_race.emails import send_captcha
from thousand_sails_race.models import UserModel
from flask import Blueprint, render_template, request, jsonify, redirect, url_for, session, flash, make_response
from thousand_sails_race.extends import mail, db
from thousand_sails_race.forms import RegisterForm, CaptchaForm, LoginForm, ForgetpawForm
from werkzeug.security import generate_password_hash

bp = Blueprint('auth', __name__, url_prefix='/auth')


@bp.route("/login", methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        email = form.email.data
        user = UserModel.query.filter_by(email=email).first()
        flash("welcome on")
        session['login'] = True
        session['user_id'] = user.id
        return redirect('/')
    return render_template('login.html', form=form)


@bp.route('/logout')
def logout():
    if 'login' in session:
        session.pop('login')
        session.pop('user_id')
        flash('成功登出')
    return redirect('/')


# GET 是从服务器获取数据
# POST：将客户端的数据提交给服务器
@bp.route("/register", methods=['GET', 'POST'])
def register():
    if 'captcha' in session:
        flash('120s 内只能进行一次注册操作')
        return redirect(url_for('auth.login'))
    form = RegisterForm()
    if form.validate_on_submit():
        email = form.email.data.lower()
        username = form.username.data
        password = form.password.data
        session['captcha'] = send_captcha(email)
        response = make_response(redirect(url_for('auth.captcha')))
        response.set_cookie(key='email', value=email, max_age=120)
        response.set_cookie(key='username', value=username, max_age=120)
        response.set_cookie(key='password', value=generate_password_hash(password), max_age=120)
        return response
    return render_template('register.html', form=form)


@bp.route('/captcha', methods=['GET', 'POST'])
def captcha():
    if 'captcha' not in session:
        return redirect('/')
    form = CaptchaForm()
    if form.validate_on_submit():
        user = UserModel(
            email=request.cookies.get('email'),
            username=request.cookies.get('username'),
            password=request.cookies.get('password')
        )
        db.session.add(user)
        db.session.commit()
        flash('注册成功')
        response = make_response(redirect('/'))
        response.delete_cookie('email')
        response.delete_cookie('username')
        response.delete_cookie('password')
        return redirect('/')
    return render_template('captcha.html', form=form)


@bp.route("/forgetpsw", methods=['GET', 'POST'])
def modify_paw():
    form = ForgetpawForm()
    if form.validate_on_submit():
        email = form.email.data
        pwd = form.password.data
        session['captcha'] = send_captcha(email)
        user = UserModel.query.filter_by(email=email).first()
        user.password = generate_password_hash(pwd)
        db.session.commit()
        return redirect('/')
    return render_template('login.html', form=form)


@bp.route("/cap")
def get_cap():
    # 从前端传回来的email
    if 'captcha' not in session:
        return redirect('/')

