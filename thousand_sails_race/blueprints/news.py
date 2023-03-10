from flask import Blueprint, render_template, g, request, flash, redirect
from thousand_sails_race.models import NewsinfoModel
from sqlalchemy.exc import ArgumentError


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
            raise ArgumentError
    except ArgumentError:
        flash('参数有误')
        return redirect('/')
    finally:
        _news = NewsinfoModel.query.filter(NewsinfoModel.id >= begin_id) \
            .filter(NewsinfoModel.id <= end_id).all()
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
        _news = NewsinfoModel.query.filter(NewsinfoModel.newstheme.contains(q)).all()
        return render_template("news.html", news=_news,begin_id=begin_id, end_id=end_id,
                               all_news_num=g.get('news_num'))
