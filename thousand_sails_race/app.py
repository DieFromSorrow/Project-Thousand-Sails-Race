from flask import Flask, session, g, render_template, flash, redirect, url_for
from thousand_sails_race import settings
from thousand_sails_race.extends import db, mail
from thousand_sails_race.models import UserModel
from thousand_sails_race.blueprints.auth import bp as auth_bp
from flask_migrate import Migrate

app = Flask(__name__)
# 绑定配置文件
app.config.from_object(settings)

db.init_app(app)
mail.init_app(app)

migrate = Migrate(app, db)

# 绑定
app.register_blueprint(auth_bp)

@app.route('/')
def demo():
    return "hello"


if __name__ == '__main__':
    app.run()