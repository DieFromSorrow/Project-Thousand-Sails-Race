
from flask import Blueprint, render_template

from thousand_sails_race.models import HotraceinfoModel, ExperienceModel, RaceinfoModel

bp = Blueprint('index', __name__)


@bp.route('/')
def index():
    hot_race = HotraceinfoModel.query.order_by(HotraceinfoModel.start_time.desc()).all()
    experience = ExperienceModel.query.limit(3).all()
    selected_race = RaceinfoModel.query.limit(10).all()
    return render_template('index.html', hot_race=hot_race,
                           experience=experience,
                           selected_race=selected_race)
