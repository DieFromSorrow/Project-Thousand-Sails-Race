
from flask import Blueprint, render_template
from thousand_sails_race.models import NewsinfoModel

bp = Blueprint('news', __name__, url_prefix='/news')


@bp.route('/')
def news():
    news = NewsinfoModel.query.all()
    return render_template('news.html', news=news)
