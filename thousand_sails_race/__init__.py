from flask import Flask, session, g, render_template, flash, redirect, url_for
from thousand_sails_race import settings
from thousand_sails_race.extends import db, mail
from thousand_sails_race.models import UserModel
from thousand_sails_race.blueprints.auth import bp as auth_bp
from thousand_sails_race.blueprints.index import bp as index_bp
from flask_migrate import Migrate

app = Flask(__name__)

# 绑定配置文件
app.config.from_object(settings)

# 删除 jinja2 渲染后前后的多余空行空格
app.jinja_env.trim_blocks = True
app.jinja_env.lstrip_blocks = True

db.init_app(app)
mail.init_app(app)

migrate = Migrate(app, db)

# 绑定
app.register_blueprint(auth_bp)
app.register_blueprint(index_bp)

