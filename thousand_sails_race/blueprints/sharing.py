
from operator import or_
from flask import Blueprint, render_template,request
from thousand_sails_race.models import ExperienceModel
from thousand_sails_race.blueprints.utils import login_verification

bp = Blueprint('sharing', __name__, url_prefix='/sharing')


@bp.route('/')
@login_verification
def sharing():
    share = ExperienceModel.query.order_by(ExperienceModel.time.desc()).all()
    return render_template('sharing.html',share=share)


@bp.route('/experience/<exper_id>')
def experice(exper_id):
    race_expe=ExperienceModel.query.get(exper_id)
    return render_template("information_page.html", race_expe=race_expe)


@bp.route("/search_experience", methods=['POST', 'GET'])
def search_sharing():
    q = str(request.args.get("q"))
    share=ExperienceModel.query.filter(or_(ExperienceModel.content.contains(q),ExperienceModel.title.contains(q))).all()
    return render_template("sharing.html", share=share)