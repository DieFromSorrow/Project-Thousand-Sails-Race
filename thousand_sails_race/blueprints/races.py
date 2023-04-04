
import json
from flask import Blueprint, render_template, request, flash, redirect, jsonify, g
from thousand_sails_race.models import RaceModel

bp = Blueprint('races', __name__, url_prefix='/races')


@bp.route('/')
def races():
    return render_template('races.html')


@bp.route('races_info')
def races_info():
    race_type = begin_id = end_id = all_num = None
    try:
        begin_id = int(request.args.get('begin_id'))
        end_id = int(request.args.get('end_id'))
        race_type = request.args.get('type')
        all_num = RaceModel.query.filter(RaceModel.type == race_type[-1]).count()
        if (begin_id < 0) or (begin_id > end_id):
            raise ValueError
    except ValueError:
        flash('参数有误')
        return redirect('/')
    finally:
        _races = RaceModel.query.filter(RaceModel.type == race_type[-1]).all()[begin_id - 1:end_id]
        _races_info = []
        for _race in _races:
            _races_info.append({
                'name': _race.name,
                'sponsor': _race.sponsor,
                'start_time': _race.start_time,
                'end_time': _race.end_time,
                'href': _race.href
            })
        return jsonify({'type': race_type, 'races_info': _races_info,
                        'begin_id': begin_id, 'end_id': end_id,
                        'all_num': all_num})

