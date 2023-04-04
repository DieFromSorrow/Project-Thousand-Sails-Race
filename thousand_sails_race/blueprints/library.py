
from flask import Blueprint, render_template, request, flash, redirect, jsonify, session, url_for
from thousand_sails_race.models import LibsModel

bp = Blueprint('library', __name__, url_prefix='/library')


@bp.route('/')
def library():
    return render_template('library.html')


@bp.route('libs_info')
def libs_info():
    lib_type = begin_id = end_id = all_num = None
    try:
        begin_id = int(request.args.get('begin_id'))
        end_id = int(request.args.get('end_id'))
        lib_type = request.args.get('type')
        all_num = LibsModel.query.filter(LibsModel.type == lib_type).count()
        if (begin_id < 0) or (begin_id > end_id) or (lib_type not in ['PPT', 'PPP', 'CQB']):
            raise ValueError
    except ValueError:
        flash('参数有误')
        return redirect('/')
    finally:
        _libs = LibsModel.query.filter(LibsModel.type == lib_type).all()[begin_id - 1:end_id]
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


@bp.route('download/<filename>')
def download(filename):
    if 'login' not in session:
        flash('请先登录')
        return redirect(url_for(endpoint='auth.login'))

    return redirect(url_for('static', filename='files/' + filename))

