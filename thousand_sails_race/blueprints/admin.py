
from flask import render_template, request, redirect, \
    url_for, session, make_response, jsonify, abort
from flask import Blueprint
import os
from functools import wraps

from thousand_sails_race.extends import db
from thousand_sails_race.models import UserModel

bp = Blueprint('admin', __name__, url_prefix='/admin')


def security_verification(func):
    """
    for the administrator authentication
    :param func: a view func
    :return warp: a safe view func
    """
    @wraps(func)
    def warp(*args, **kwargs):
        if 'admin' not in session:
            abort(403)
        return func(*args, **kwargs)

    return warp


@bp.route('/')
def index():
    return render_template('admin_index.html')


@bp.route('/login', methods=['POST'])
def login():
    if request.form.get('username') != 'admin' or \
            request.form.get('password') != \
            os.getenv('ADMIN_PASSWORD'):
        return redirect(url_for('admin.index'))
    session['admin'] = True
    return redirect(url_for('admin.dashboard'))


@bp.route('/dashboard')
def dashboard():
    # Render admin dashboard here
    apis = {
        '用户管理界面': url_for('admin.users_administration')
    }
    return render_template('admin_dashboard.html')


@bp.route('/dashboard/users_administration')
def users_administration():
    users = UserModel.query.all()
    return render_template('admin_users_administration.html', users=users)


@bp.route('/dashboard/users_administration/delete_user', methods=['DELETE'])
@security_verification
def delete_user():
    data = request.get_json()
    _id = data.get('id')
    user = UserModel.query.get(_id)
    db.session.delete(user)
    db.session.commit()
    return jsonify({'success': True})


@bp.route('/dashboard/users_administration/modify_user', methods=['PUT'])
@security_verification
def modify_user():
    return jsonify({'success': True})


@bp.route('/dashboard/users_administration/user/<userid>', methods=['GET'])
@security_verification
def get_user(userid):
    user = UserModel.query.filter(UserModel.id == userid).first()
    return jsonify({'success': True,
                    'username': user.username,
                    'email': user.email})

