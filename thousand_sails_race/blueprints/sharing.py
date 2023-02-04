
from flask import Blueprint, render_template

bp = Blueprint('sharing', __name__, url_prefix='/sharing')


@bp.route('/')
def sharing():
    return render_template('sharing.html')
