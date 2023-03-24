from flask import Blueprint, render_template

from thousand_sails_race.models import HotraceinfoModel, ExperienceModel, RaceinfoModel

bp = Blueprint('index', __name__)


@bp.route('/')
def index():
    hot_race = HotraceinfoModel.query.order_by(HotraceinfoModel.start_time.desc()).all()
    experience = ExperienceModel.query.limit(3).all()
    selected_race = RaceinfoModel.query.limit(10).all()
    return render_template('index.html', hot_race=hot_race,experience=experience,selected_race=selected_race)


@bp.route('/hotrace/<racename_id>')
def hotrace(racename_id):
    race = HotraceinfoModel.query.get(racename_id)
    return render_template("sharing_page.html", race=race)


@bp.route('/races_10/<racename_id>')
def races_10(racename_id):
    race = RaceinfoModel.query.get(racename_id)
    return render_template("sharing_page.html", race=race)


