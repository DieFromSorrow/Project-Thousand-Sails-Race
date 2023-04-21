from flask import Flask, session, g

from thousand_sails_race import settings
from thousand_sails_race.extends import db, mail

from thousand_sails_race.blueprints.auth import bp as auth_bp
from thousand_sails_race.blueprints.news import bp as news_bp
from thousand_sails_race.blueprints.index import bp as index_bp
from thousand_sails_race.blueprints.races import bp as races_bp
from thousand_sails_race.blueprints.sharing import bp as sharing_bp
from thousand_sails_race.blueprints.library import bp as library_bp
from thousand_sails_race.blueprints.admin import bp as admin_bp
from thousand_sails_race.blueprints.forum import bp as forum_bp
from flask_migrate import Migrate
from thousand_sails_race.models import UserModel, QuestionModel


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
app.register_blueprint(forum_bp)

register_commands()


@app.template_filter('replace1')
def replace1(value):
    return value.replace(' ', '//n')


@app.before_request
def my_before_request():
    user_id = session.get("user_id")
    if user_id:
        user_who = UserModel.query.get(user_id)
        setattr(g, "user_who", user_who)
    else:
        setattr(g, "user_who", None)


# 上下文处理器：定义为全局变量
@app.context_processor
def my_context_process():
    return {"user_who": g.user_who}
