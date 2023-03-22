
from flask import Blueprint, render_template

bp = Blueprint('forum', __name__, url_prefix='/forum')


@bp.route('/')
def forum():
    return render_template('forum.html')
