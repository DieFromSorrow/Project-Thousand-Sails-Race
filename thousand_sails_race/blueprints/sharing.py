
from flask import Blueprint, render_template

from thousand_sails_race.models import ExperienceModel

bp = Blueprint('sharing', __name__, url_prefix='/sharing')


@bp.route('/')
def sharing():
    return render_template('sharing.html')


@bp.route('/experience/<exper_id>')
def experice(exper_id):
    race_expe=ExperienceModel.query.get(exper_id)
    return render_template("information_page.html", race_expe=race_expe)