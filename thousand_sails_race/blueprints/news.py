
from flask import Blueprint, render_template, g, request, flash, redirect
from thousand_sails_race.models import NewsinfoModel

bp = Blueprint('news', __name__, url_prefix='/news')


@bp.before_request
def get_news_num():
    news_num = NewsinfoModel.query.count()
    g.news_num = news_num


@bp.route('/')
def news():
    begin_id = end_id = None
    try:
        begin_id = int(request.args.get('begin_id'))
        end_id = int(request.args.get('end_id'))
        if (begin_id < 0) or (begin_id > end_id):
            raise ValueError
    except ValueError:
        flash('参数有误')
        return redirect('/')
    finally:
        _news = NewsinfoModel.query.filter(NewsinfoModel.id >= begin_id) \
            .filter(NewsinfoModel.id <= end_id).all()
        return render_template('news.html', news=_news,
                               begin_id=begin_id, end_id=end_id,
                               all_news_num=g.get('news_num'))
