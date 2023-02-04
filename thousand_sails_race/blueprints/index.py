
from flask import Blueprint, render_template, request, jsonify, redirect, url_for, session, flash

bp = Blueprint('index', __name__)


@bp.route('/')
def index():
    return render_template('index.html')