from flask_wtf import FlaskForm
import wtforms
from wtforms.validators import Email, Length, EqualTo, InputRequired
from thousand_sails_race.models import UserModel, EmailCaptchaModel
from werkzeug.security import generate_password_hash, check_password_hash
from flask import session
from thousand_sails_race.extends import db


# Form:主要是用来验证前端提交的表单数据是否符合要求
class RegisterForm(FlaskForm):
    email = wtforms.StringField(validators=[Email(message="邮箱格式错误！")])
    username = wtforms.StringField(validators=[Length(min=3, max=20, message="用户名格式错误！")])
    password = wtforms.StringField(validators=[Length(min=6, max=20, message="密码格式错误！")])
    password_confirm = wtforms.StringField(validators=[EqualTo("password")])
    submit = wtforms.SubmitField('注册')

    def validate_email(self, field):
        email = field.data.lower()
        user = UserModel.query.filter_by(email=email).first()
        if user:
            raise wtforms.ValidationError(message="该邮箱已被注册")


class CaptchaForm(FlaskForm):
    captcha = wtforms.StringField(validators=[Length(min=4, max=4, message="验证码格式错误！")])
    submit = wtforms.SubmitField('验证')

    def validate_captcha(self, field):
        captcha = field.data
        if 'captcha' not in session:
            raise wtforms.ValidationError(message='请获取验证码')
        elif session['captcha'] != captcha:
            raise wtforms.ValidationError(message='验证码错误')
        session.pop('captcha')


class LoginForm(FlaskForm):
    email = wtforms.StringField(validators=[Email(message="邮箱格式错误！")])
    password = wtforms.StringField(validators=[Length(min=6, max=20, message="密码格式错误！")])
    submit = wtforms.SubmitField('登录')

    def validate_email(self, field):
        email = field.data
        user = UserModel.query.filter_by(email=email).first()
        if not user:
            raise wtforms.ValidationError(message='用户不存在')

    def validate_password(self, field):
        email = self.email.data
        password = field.data
        user = UserModel.query.filter_by(email=email).first()
        if user:
            if not check_password_hash(user.password, password):
                raise wtforms.ValidationError(message='密码错误')