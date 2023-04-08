

from flask import Blueprint, render_template, g, request, flash, redirect,url_for, session

from thousand_sails_race import db
from thousand_sails_race.forms import AnswerForm, QuestionForm
from thousand_sails_race.models import QuestionModel, AnswerModel

bp = Blueprint('forum', __name__, url_prefix='/forum')


@bp.route('/')
def forum():
    questions = QuestionModel.query.order_by(QuestionModel.create_time.desc()).all()
    return render_template('forum.html', questions=questions)


@bp.route('/forum_details/<ques_id>')
def forum_question(ques_id):
    question = QuestionModel.query.get(ques_id)
    if session.get('user_id') != question.author_id:
        question.view_num += 1
        pass
    return render_template("forum_details.html", question=question)


@bp.route("/search_forum", methods=['POST', 'GET'])
def search_question():
    q = str(request.args.get("q"))
    forums = QuestionModel.query.filter(QuestionModel.title.contains(q)).all()
    return render_template("forum.html", questions=forums)


@bp.route("/answer/public", methods=['POST'])
def public_answer():
    form = AnswerForm(request.form)
    if form.validate():
        content = form.content.data
        question_id = form.question_id.data
        answer = AnswerModel(content=content, question_id=question_id, author_id=g.user_who.id)
        db.session.add(answer)
        db.session.commit()
        return redirect(url_for("forum.forum_question", ques_id=question_id))
    else:
        print(form.errors)
        return redirect(url_for("forum.forum_question", ques_id=request.form.get("question_id")))


# 发布问答的页面
@bp.route("/publish", methods=["GET", "POST"])
def publish_question():
    if not g.user_who:
        return redirect(url_for("auth.login"))
    if request.method == "GET":
        return render_template("publish.html")
    else:
        form = QuestionForm(request.form)
        if form.validate():
            title = form.title.data
            content = form.content.data
            question = QuestionModel(title=title, content=content, author=g.user_who)
            db.session.add(question)
            db.session.commit()
            # 跳转到这篇问答的详情页
            return redirect(url_for("forum.forum"))
        else:
            print(form.errors)
            return redirect(url_for("forum.publish_question"))
