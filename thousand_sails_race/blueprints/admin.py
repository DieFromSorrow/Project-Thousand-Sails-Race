
from flask import Blueprint, render_template, request, redirect, \
    url_for, session, make_response, jsonify, abort

import os
from functools import wraps
from thousand_sails_race.models import *
from thousand_sails_race.extends import db

bp = Blueprint('admin', __name__, url_prefix='/admin')


def security_verification(func):
    """
    for the administrator authentication
    :param func: a view func
    :return warp: a safe view func
    """
    @wraps(func)
    def wrapper(*args, **kwargs):
        if 'admin' not in session:
            abort(403)
        return func(*args, **kwargs)

    return wrapper


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
        '用户管理界面': url_for('admin.administer_user'),
        '竞赛信息管理': url_for('admin.administer_race'),
        '热门竞赛管理': url_for('admin.administer_hot_race'),
        '新闻管理界面': url_for('admin.administer_news'),
        '资源内容管理': url_for('admin.administer_lib'),
        '经验分享管理': url_for('admin.administer_exp'),
        '论坛问题管理': url_for('admin.administer_qst'),
        '论坛评论管理': url_for('admin.administer_ans')
    }
    return render_template('admin_dashboard.html', apis=apis)


class GenerateAdminViewFunctions:
    def __init__(self, api_name, model_class, table_dict, title, addable=True):
        self.api_name = api_name
        self.model_class = model_class
        self.table_dict = table_dict
        self.title = title
        self.addable = addable
        pass

    def __call__(self, func):
        @security_verification
        def administer():
            data = self.model_class.query.all()
            return render_template('administration.html', api_name=self.api_name,
                                   data=data, title=self.title, table_dict=self.table_dict,
                                   addable=self.addable)

        @security_verification
        def delete():
            _id = request.args.get('_id')
            item = self.model_class.query.get(_id)
            if item:
                db.session.delete(item)
                db.session.commit()
                pass
            else:
                abort(404)
            return jsonify({'success': True})

        @security_verification
        def modify():
            _id = request.args.get('_id')
            data = request.get_json()
            item = self.model_class.query.get(_id)
            if item:
                for column, value in data.items():
                    if value != getattr(item, column):
                        setattr(item, column, value)
                db.session.commit()
                pass
            else:
                abort(404)
            return jsonify({'success': True})

        @security_verification
        def add():
            data = request.get_json()
            item = self.model_class(**data)
            db.session.add(item)
            db.session.commit()
            return jsonify({'success': True})

        @security_verification
        def get():
            response = None
            _id = request.args.get('_id')
            item = self.model_class.query.get(_id)
            item_dict = {}
            for column in item.__table__.columns:
                if column.name in self.table_dict and self.table_dict[column.name]['changeable']:
                    value = getattr(item, column.name)
                    if self.table_dict[column.name]['type'] == 'datetime-local':
                        value = value.isoformat()
                    item_dict[column.name] = value
            if item:
                response = {'success': True}
                response.update(item_dict)
                pass
            else:
                abort(404)
            return jsonify(response)

        view_func_list = [administer, delete, modify, add, get]
        method_list = ['GET', 'DELETE', 'POST', 'POST', 'GET']

        for idx, view_func in enumerate(view_func_list):
            view_func.__name__ += '_' + self.api_name
            bp.add_url_rule(f'/dashboard/{self.api_name}_administration/{view_func.__name__}',
                            view_func=view_func, methods=[method_list[idx]])
            pass

        return func


@GenerateAdminViewFunctions(
    api_name='user', model_class=UserModel, title='User Management', addable=False,
    table_dict={
        'username': {'table_head': 'Username', 'changeable': True, 'display': True, 'type': 'text'},
        'email': {'table_head': 'Email', 'changeable': True, 'display': True, 'type': 'email'},
        'join_time': {'table_head': 'Registration Time', 'changeable': False, 'display': True, 'type': 'datetime-local'}
    })
def admin_user_view():
    pass


@GenerateAdminViewFunctions(
    api_name='news', model_class=NewsModel, title='News Management',
    table_dict={
        'news_theme': {'table_head': 'Theme', 'changeable': True, 'display': True, 'type': 'text'},
        'news_content': {'table_head': 'Content', 'changeable': True, 'display': False, 'type': 'textarea'},
        'news_time': {'table_head': 'Time', 'changeable': True, 'display': True, 'type': 'datetime-local'}
    })
def admin_news_view():
    pass


@GenerateAdminViewFunctions(
    api_name='race', model_class=RaceModel, title='Race Management',
    table_dict={
        'name': {'table_head': 'Name', 'changeable': True, 'display': True, 'type': 'text'},
        'sponsor': {'table_head': 'Sponsor', 'changeable': True, 'display': True, 'type': 'text'},
        'type': {'table_head': 'Type', 'changeable': True, 'display': True, 'type': 'text'},
        'start_time': {'table_head': 'Start Time', 'changeable': True, 'display': True, 'type': 'datetime-local'},
        'end_time': {'table_head': 'End Time', 'changeable': True, 'display': True, 'type': 'datetime-local'},
        'details': {'table_head': 'Details', 'changeable': True, 'display': False, 'type': 'textarea'},
        'href': {'table_head': 'URL', 'changeable': True, 'display': False, 'type': 'text'}
    })
def admin_race_view():
    pass


@GenerateAdminViewFunctions(
    api_name='lib', model_class=LibsModel, title='Library Management',
    table_dict={
        'name': {'table_head': 'Name', 'changeable': True, 'display': True, 'type': 'text'},
        'type': {'table_head': 'Type', 'changeable': True, 'display': True, 'type': 'text'},
        'time': {'table_head': 'Upload Time', 'changeable': True, 'display': True, 'type': 'datetime-local'},
        'href': {'table_head': 'URL', 'changeable': True, 'display': False, 'type': 'text'}
    })
def admin_lib_view():
    pass


@GenerateAdminViewFunctions(
    api_name='hot_race', model_class=HotRaceModel, title='Hot Race Management',
    table_dict={
        'name': {'table_head': 'Name', 'changeable': True, 'display': True, 'type': 'text'},
        'sponsor': {'table_head': 'Sponsor', 'changeable': True, 'display': True, 'type': 'text'},
        'type': {'table_head': 'Type', 'changeable': True, 'display': True, 'type': 'text'},
        'start_time': {'table_head': 'Start Time', 'changeable': True, 'display': True, 'type': 'datetime-local'},
        'end_time': {'table_head': 'End Time', 'changeable': True, 'display': True, 'type': 'datetime-local'},
        'details': {'table_head': 'Details', 'changeable': True, 'display': False, 'type': 'textarea'},
        'href': {'table_head': 'URL', 'changeable': True, 'display': False, 'type': 'text'}
    })
def admin_hot_race_view():
    pass


@GenerateAdminViewFunctions(
    api_name='exp', model_class=ExperienceModel, title='经验分享管理界面',
    table_dict={
        'title': {'table_head': '标题', 'changeable': True, 'display': True, 'type': 'text'},
        'type': {'table_head': '类型', 'changeable': True, 'display': True, 'type': 'text'},
        'content': {'table_head': '内容', 'changeable': True, 'display': False, 'type': 'textarea'},
        'time': {'table_head': '上传时间', 'changeable': True, 'display': True, 'type': 'datetime-local'},
        'author_id': {'table_head': '作者ID', 'changeable': False, 'display': True, 'type': 'text'},
        'all_race_id': {'table_head': '对应竞赛ID', 'changeable': True, 'display': True, 'type': 'text'},
        'hot_race_id': {'table_head': '热门竞赛ID', 'changeable': True, 'display': True, 'type': 'text'}
    })
def admin_exp_view():
    pass


@GenerateAdminViewFunctions(
    api_name='qst', model_class=QuestionModel, title='Question Management',
    table_dict={
        'title': {'table_head': 'Title', 'changeable': True, 'display': True, 'type': 'text'},
        'content': {'table_head': 'Content', 'changeable': True, 'display': False, 'type': 'textarea'},
        'create_time': {'table_head': 'Creating Time', 'changeable': True, 'display': True, 'type': 'datetime-local'},
        'view_num': {'table_head': 'View Num', 'changeable': False, 'display': True, 'type': 'text'},
        'author_id': {'table_head': 'Author Id', 'changeable': False, 'display': True, 'type': 'text'}
    })
def admin_qst_view():
    pass


@GenerateAdminViewFunctions(
    api_name='ans', model_class=AnswerModel, title='Answer Management',
    table_dict={
        'content': {'table_head': 'Content', 'changeable': True, 'display': False, 'type': 'textarea'},
        'create_time': {'table_head': 'Creating Time', 'changeable': True, 'display': True, 'type': 'datetime-local'},
        'question_id': {'table_head': 'Question ID', 'changeable': False, 'display': True, 'type': 'text'},
        'author_id': {'table_head': 'Question ID', 'changeable': False, 'display': True, 'type': 'text'}
    })
def admin_ans_view():
    pass





