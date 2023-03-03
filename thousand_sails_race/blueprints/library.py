
from flask import Blueprint, render_template, request, flash, redirect, jsonify
from thousand_sails_race.models import LibsinfoModel

bp = Blueprint('library', __name__, url_prefix='/library')


@bp.route('/')
def library():
    return render_template('library.html')


@bp.route('libs_info')
def races_info():
    lib_type = begin_id = end_id = all_num = None
    try:
        begin_id = int(request.args.get('begin_id'))
        end_id = int(request.args.get('end_id'))
        lib_type = request.args.get('type')
        all_num = LibsinfoModel.query.filter(LibsinfoModel.type == lib_type).count()
        if (begin_id < 0) or (begin_id > end_id) or (lib_type not in ['PPT', 'PPP', 'CQB']):
            raise ValueError
    except ValueError:
        flash('参数有误')
        return redirect('/')
    finally:
        _libs = LibsinfoModel.query.filter(LibsinfoModel.type == lib_type).all()[begin_id-1:end_id]
        _libs_info = []
        for _lib in _libs:
            _libs_info.append({
                'name': _lib.name,
                'time': _lib.time,
                'href': _lib.href
            })
        return jsonify({'type': lib_type, 'libs_info': _libs_info,
                        'begin_id': begin_id, 'end_id': end_id,
                        'all_num': all_num})
