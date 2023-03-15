
from flask import Blueprint, render_template, request, jsonify, redirect, url_for, session, flash

from thousand_sails_race.models import HotraceinfoModel, ExperienceModel, RaceinfoModel

bp = Blueprint('index', __name__)


@bp.route('/')
def index():
    hotrace = HotraceinfoModel.query.order_by(HotraceinfoModel.start_time.desc()).all()
    experience = ExperienceModel.query.limit(3).all()
    selected_race=RaceinfoModel.query.limit(10).all()
    return render_template('index.html',hot_race=hotrace,experience=experience,selected_race=selected_race)