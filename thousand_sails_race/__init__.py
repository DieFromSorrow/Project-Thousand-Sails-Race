from flask import Flask

from thousand_sails_race import settings
from thousand_sails_race.extends import db, mail

from thousand_sails_race.blueprints.auth import bp as auth_bp
from thousand_sails_race.blueprints.news import bp as news_bp
from thousand_sails_race.blueprints.index import bp as index_bp
from thousand_sails_race.blueprints.races import bp as races_bp
from thousand_sails_race.blueprints.sharing import bp as sharing_bp
from thousand_sails_race.blueprints.library import bp as library_bp
from thousand_sails_race.blueprints.admin import bp as admin_bp

from flask_migrate import Migrate


def register_commands():
    from thousand_sails_race import commands


app = Flask('thousand_sails_race')

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
app.register_blueprint(news_bp)
app.register_blueprint(index_bp)
app.register_blueprint(races_bp)
app.register_blueprint(sharing_bp)
app.register_blueprint(library_bp)
app.register_blueprint(admin_bp)

register_commands()
