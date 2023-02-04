
from flask import Blueprint, render_template

bp = Blueprint('races', __name__, url_prefix='/races')


@bp.route('/')
def races():
    return render_template('races.html')
