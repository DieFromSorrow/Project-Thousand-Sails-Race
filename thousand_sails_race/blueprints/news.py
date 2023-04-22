
from operator import or_
from flask import Blueprint, render_template, g, request, flash, redirect
from thousand_sails_race.models import NewsModel
from sqlalchemy.exc import ArgumentError
from thousand_sails_race.blueprints.utils import login_verification


bp = Blueprint('news', __name__, url_prefix='/news')


@bp.before_request
def get_news_num():
    news_num = NewsModel.query.count()
    g.news_num = news_num


@bp.route('/')
@login_verification
def news():
    begin_id = end_id = None
    try:
        begin_id = int(request.args.get('begin_id'))
        end_id = int(request.args.get('end_id'))
        if (begin_id < 0) or (begin_id > end_id):
            raise ArgumentError
    except ArgumentError:
        flash('参数有误')
        return redirect('/')
    finally:
        _news = NewsModel.query.filter(NewsModel.id >= begin_id) \
            .filter(NewsModel.id <= end_id).all()
        return render_template('news.html', news=_news,
                               begin_id=begin_id, end_id=end_id,
                               all_news_num=g.get('news_num'))


@bp.route("/search", methods=['POST', 'GET'])
def search():
    # q = str(request.args.get("q"))
    # new=NewsinfoModel.query.filter(or_(NewsinfoModel.title.contains(q),NewsinfoModel.content.contains(q))).all()
    # _news=NewsinfoModel.query.filter(NewsinfoModel.title.contains(q)).all()
    # return render_template("news.html", news=_news)
    q = str(request.args.get("q"))
    begin_id = end_id = 0
    try:
        begin_id = int(request.args.get('begin_id'))
        end_id = int(request.args.get('end_id'))
        if (begin_id < 0) or (begin_id > end_id):
            raise ValueError
    except ValueError:
        flash('参数有误')
        return redirect('/')
    finally:
        _news = NewsModel.query.filter(or_(NewsModel.news_theme.contains(q),NewsModel.news_content.contains(q))).all()
        return render_template("news.html", news=_news,begin_id=begin_id, end_id=end_id,
                               all_news_num=g.get('news_num'))


@bp.route('/news/<news_id>')
def news_info(news_id):
    _news = NewsModel.query.get(news_id)
    return render_template("news_page.html", news=_news)

