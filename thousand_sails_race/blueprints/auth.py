from thousand_sails_race.emails import send_captcha
from thousand_sails_race.models import UserModel
from flask import Blueprint, render_template, request, jsonify, redirect, url_for, session, flash, make_response
from thousand_sails_race.extends import mail, db
from thousand_sails_race.forms import RegisterForm, LoginForm, ForgetpawForm
from werkzeug.security import generate_password_hash
import time

bp = Blueprint('auth', __name__, url_prefix='/auth')


@bp.route('/<string:action>', methods=['GET', 'POST'])
def auth(action):

    login_form = LoginForm()
    register_form = RegisterForm()
    forget_pw_form = ForgetpawForm()

    if action == 'login' and login_form.validate_on_submit():
        email = login_form.email.data
        user = UserModel.query.filter_by(email=email).first()
        flash('登陆成功')
        session['login'] = True
        session['user_id'] = user.id
        return redirect('/')

    if action == 'register' and register_form.validate_on_submit():
        email = register_form.email.data.lower()
        username = register_form.username.data
        password = register_form.password.data
        user = UserModel(
            username=username,
            password=generate_password_hash(password),
            email=email
        )
        session['login'] = True
        session['user_id'] = user.id
        db.session.add(user)
        db.session.commit()
        flash('注册成功')
        return redirect('/')

    if action == 'modify' and forget_pw_form.validate_on_submit():
        email = forget_pw_form.email.data
        password = forget_pw_form.password.data
        user = UserModel.query.filter_by(email=email).first()
        user.password = generate_password_hash(password)
        db.session.commit()
        session['login'] = True
        session['user_id'] = user.id
        flash('修改成功')
        return redirect('/')

    return render_template('login_new.html', login_form=login_form,
                           register_form=register_form, forget_pw_form=forget_pw_form)


@bp.route('/send_verification_code', methods=['POST'])
def send_verification_code():
    data = request.get_json()
    email = data.get('email')
    if not email:
        return {'success': False, 'message': 'Email is required'}, 400

    # 将验证码存储在 session 中，有效期为 120 秒
    session['verification_code'] = send_captcha(receptions=email)
    print(session.get('verification_code'))

    return {'success': True, 'message': 'Verification code sent successfully'}, 200


@bp.route('/logout')
def logout():
    if 'login' in session:
        session.pop('login')
        session.pop('user_id')
        flash('成功登出')
    return redirect('/')

