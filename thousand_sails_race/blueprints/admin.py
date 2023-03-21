
from flask import Flask, render_template, request, redirect, url_for
from flask import Blueprint
import os

bp = Blueprint('admin', __name__, url_prefix='/admin')


@bp.route('/')
def index():
    return render_template('admin_index.html')


@bp.route('/login', methods=['POST'])
def login():
    if request.form.get('username') != 'admin' or \
            request.form.get('password') != \
            os.getenv('ADMIN_PASSWORD'):
        return redirect(url_for('admin.index'))
    return redirect(url_for('admin.admin'))


@bp.route('/admin')
def admin():
    # Render admin dashboard here
    return "Admin Dashboard"
