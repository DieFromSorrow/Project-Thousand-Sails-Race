
from flask import Blueprint, render_template

from thousand_sails_race.models import QuestionModel

bp = Blueprint('forum', __name__, url_prefix='/forum')


@bp.route('/')
def forum():
    questions = QuestionModel.query.order_by(QuestionModel.create_time.desc()).all()
    return render_template('forum.html',questions=questions)

@bp.route('/public')
def forum_question():
    return
