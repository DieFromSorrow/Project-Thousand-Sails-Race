from operator import or_

from flask import Blueprint, render_template, g, request, redirect,url_for, \
    session, flash, jsonify

from thousand_sails_race import db
from thousand_sails_race.forms import AnswerForm, QuestionForm
from thousand_sails_race.models import QuestionModel, AnswerModel, UserModel
from thousand_sails_race.blueprints.utils import login_verification


bp = Blueprint('forum', __name__, url_prefix='/forum')


@bp.route('/')
@login_verification
def forum():
    questions = QuestionModel.query.order_by(QuestionModel.create_time.desc()).all()
    return render_template('forum.html', questions=questions)


@bp.route('/forum_details/<qst_id>')
def forum_question(qst_id):
    question = QuestionModel.query.get(qst_id)
    is_liked = g.get('user_who') in question.like_user
    liked_num = len(question.like_user)
    if session.get('user_id') != question.author_id:
        question.view_num += 1
        db.session.commit()
        pass
    return render_template("forum_details.html", question=question, is_liked=is_liked, liked_num=liked_num)


@bp.route('/search_forum', methods=['POST', 'GET'])
def search_question():

    # q = str(request.args.get("q"))
    # q = str(request.args.get("q"))
    # forums=QuestionModel.query.filter(QuestionModel.title.contains(q)).all()
    # forums = QuestionModel.query.whooshee_search(q)
    # return render_template("forum.html", questions=forums)

    q = str(request.args.get("q"))
    forums = QuestionModel.query.filter(or_(QuestionModel.title.contains(q),QuestionModel.content.contains(q))).all()
    return render_template('forum.html', questions=forums)


@bp.route('/answer/public', methods=['POST'])
@login_verification
def public_answer():
    form = AnswerForm(request.form)
    if form.validate():
        content = form.content.data
        question_id = form.question_id.data
        answer = AnswerModel(content=content, question_id=question_id, author_id=g.user_who.id)
        db.session.add(answer)
        db.session.commit()
        return redirect(url_for('forum.forum_question', qst_id=question_id))
    else:
        print(form.errors)
        return redirect(url_for('forum.forum_question', qst_id=request.form.get("question_id")))


# 发布问答的页面
@bp.route('/publish', methods=['GET', 'POST'])
@login_verification
def publish_question():
    if request.method == 'GET':
        return render_template('publish.html')
    else:
        form = QuestionForm(request.form)
        if form.validate():
            title = form.title.data
            content = form.content.data
            question = QuestionModel(title=title, content=content, author=g.user_who)
            db.session.add(question)
            db.session.commit()
            # 跳转到这篇问答的详情页
            return redirect(url_for('forum.forum'))
        else:
            print(form.errors)
            return redirect(url_for('forum.publish_question'))


@bp.route('/like_qst', methods=['POST'])
@login_verification
def like_qst():
    data = request.get_json()
    qst_id = data['qst_id'][0]
    qst = QuestionModel.query.get(qst_id)
    if qst:
        if data['liked']:
            usr = g.get('user_who')
            qst.like_user.remove(usr)
            db.session.commit()
            pass
        else:
            usr = g.get('user_who')
            qst.like_user.append(usr)
            db.session.commit()
            pass
    return jsonify({'success': True})

