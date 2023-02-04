
from flask import Blueprint, render_template

bp = Blueprint('library', __name__, url_prefix='/library')


@bp.route('/')
def library():
    return render_template('library.html')
