# 存放扩展文件--解决循环引用的问题
from flask_sqlalchemy import SQLAlchemy
from flask_mail import Mail
from flask_whooshee import Whooshee
whooshee=Whooshee()

db = SQLAlchemy()
mail = Mail()
