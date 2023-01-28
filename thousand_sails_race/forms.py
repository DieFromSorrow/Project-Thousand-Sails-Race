import wtforms
from wtforms.validators import Email, Length, EqualTo, InputRequired
from thousand_sails_race.models import UserModel, EmailCaptchaModel
from thousand_sails_race.extends import db

# Form:主要是用来验证前端提交的表单数据是否符合要求
class RegisterForm(wtforms.Form):
    email = wtforms.StringField(validators=[Email(message="邮箱格式错误！")])
    captcha = wtforms.StringField(validators=[Length(min=4, max=4, message="验证码格式错误！")])
    username = wtforms.StringField(validators=[Length(min=3, max=20, message="用户名格式错误！")])
    password = wtforms.StringField(validators=[Length(min=6, max=20, message="密码格式错误！")])
    password_confirm = wtforms.StringField(validators=[EqualTo("password")])

    def validate_email(self, field):
        email = field.data
        user = UserModel.query.filter_by(email=email).first()
        if user:
            raise wtforms.ValidationError(message="该邮箱已被注册")

    # 自定义验证
    # 邮箱是否已经被注册
    # 验证码是否正确
    # def validate_email(self, field):
    #     email = field.data
    #     user = UserModel.query.filter_by(email=email).first()
    #     if user:
    #         raise wtforms.ValidationError(message="该邮箱已被注册")

    # 验证码是否正确
    def validate_captcha(self, field):
        captcha = field.data
        email = self.email.data
        captcha_model = EmailCaptchaModel.query.filter_by(email=email, captcha=captcha).first()
        if not captcha_model:
            raise wtforms.ValidationError(message="邮箱验证码错误！")
        # 可以删掉captcha_model,时间慢

        # else:
        #     db.session.delete(captcha_model)
        #     db.session.commit()


class LoginForm(wtforms.Form):
    email = wtforms.StringField(validators=[Email(message="邮箱格式错误！")])
    password = wtforms.StringField(validators=[Length(min=6, max=20, message="密码格式错误！")])
