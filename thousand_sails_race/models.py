from thousand_sails_race.extends import db
from datetime import datetime
from werkzeug.security import generate_password_hash


# 用户信息表
class UserModel(db.Model):
    __tablename__ = "user"
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    username = db.Column(db.String(100), nullable=False)
    password = db.Column(db.String(200), nullable=False)
    email = db.Column(db.String(100), nullable=False, unique=True)
    join_time = db.Column(db.DateTime, default=datetime.now)
    exp = db.relationship('ExperienceModel', back_populates='author')
    questions = db.relationship('QuestionModel', back_populates='author')
    answers = db.relationship('AnswerModel', back_populates='author')

    def set_password(self, password):
        self.password = generate_password_hash(password)


# 赛事表--id,竞赛名称、主办方、开始时间、结束时间、竞赛详情
class RaceModel(db.Model):
    __tablename__ = "raceinfo"
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(100), nullable=False)
    sponsor = db.Column(db.String(100), nullable=False)
    type = db.Column(db.String(50), nullable=False)
    start_time = db.Column(db.DateTime)
    end_time = db.Column(db.DateTime)
    details = db.Column(db.Text, nullable=False)
    href = db.Column(db.String(200), nullable=False)
    exp = db.relationship('ExperienceModel', back_populates='race_all')
    news = db.relationship('NewsModel', back_populates='race')


# 热门赛事
class HotRaceModel(db.Model):
    __tablename__ = "hotraceinfo"
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(100), nullable=False)
    sponsor = db.Column(db.String(100), nullable=False)
    type = db.Column(db.String(50), nullable=False)
    start_time = db.Column(db.DateTime)
    end_time = db.Column(db.DateTime)
    details = db.Column(db.Text, nullable=False)
    href = db.Column(db.String(200), nullable=False)
    exp = db.relationship('ExperienceModel', back_populates='race_hot')


class LibsModel(db.Model):
    __tablename__ = "libsinfo"
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(100), nullable=False)
    type = db.Column(db.String(50), nullable=False)
    time = db.Column(db.DateTime)
    href = db.Column(db.String(200), nullable=False)


# 新闻公告表--id,新闻主题、新闻内容、发布时间
class NewsModel(db.Model):
    __tablename__ = "newsinfo"
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    news_theme = db.Column(db.String(200), nullable=False)
    news_content = db.Column(db.Text, nullable=False)
    news_time = db.Column(db.DateTime)

    # 外键--新闻公告对应的某个比赛
    race_info_id = db.Column(db.Integer, db.ForeignKey("raceinfo.id"))
    race = db.relationship('RaceModel', back_populates="news")


# 经验贴--id,经验类型、发布时间
class ExperienceModel(db.Model):
    __tablename__ = "experinfo"
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    type = db.Column(db.String(200), nullable=False)
    title = db.Column(db.String(200), nullable=False)
    content = db.Column(db.Text, nullable=False)
    time = db.Column(db.DateTime)

    # 外键--发表人
    author_id = db.Column(db.Integer, db.ForeignKey("user.id"))
    hot_race_id = db.Column(db.Integer, db.ForeignKey("hotraceinfo.id"))
    all_race_id = db.Column(db.Integer, db.ForeignKey("raceinfo.id"))

    author = db.relationship('UserModel', back_populates="exp")
    race_hot = db.relationship('HotRaceModel', back_populates="exp")
    race_all = db.relationship('RaceModel', back_populates="exp")


# 发表问题--id,题目、内容、发表时间
class QuestionModel(db.Model):
    __tablename__ = "question"
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    title = db.Column(db.String(100), nullable=False)
    content = db.Column(db.Text, nullable=False)
    create_time = db.Column(db.DateTime, default=datetime.now)
    view_num = db.Column(db.Integer, nullable=False, default=0)
    # 隐式属性
    # answers = db.relationship('AnswerModel', back_populates='question')

    # 外键--发表人
    author_id = db.Column(db.Integer, db.ForeignKey("user.id"))
    author = db.relationship('UserModel', back_populates="questions")


# 针对问题进行评论--id,内容、创建时间
class AnswerModel(db.Model):
    __tablename__ = "answer"
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    content = db.Column(db.Text, nullable=False)
    create_time = db.Column(db.DateTime, default=datetime.now())

    # 外键--问题、作者
    question_id = db.Column(db.Integer, db.ForeignKey("question.id"))
    author_id = db.Column(db.Integer, db.ForeignKey("user.id"))

    # 关系
    question = db.relationship(QuestionModel, backref=db.backref("answers", order_by=create_time.desc()))
    author = db.relationship('UserModel', back_populates="answers")
