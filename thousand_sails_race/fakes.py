import random
import time

from faker import Faker
from thousand_sails_race.models import *
from thousand_sails_race.extends import db

fake = Faker('zh_CN')


def fake_admin():
    user = UserModel(
        username='lys',
        email='2937128647@qq.com',
        join_time=fake.date_time_this_month(
            before_now=True,
            after_now=False,
            tzinfo=None
        )
    )
    user.set_password(password='QQ2937128647')
    db.session.add(user)
    db.session.commit()
    pass


def fake_user(count=30):
    for i in range(count):
        user = UserModel(
            username=fake.user_name(),
            email=fake.email(),
            join_time=fake.date_time_this_month(
                before_now=True,
                after_now=False,
                tzinfo=None
            )
        )
        user.set_password(password='123456789')
        db.session.add(user)
        pass
    db.session.commit()
    pass


def fake_race(count=160):
    for i in range(count):
        race = RaceModel(
            name=fake.sentence(
                nb_words=8,
                variable_nb_words=True,
                ext_word_list=None
            ),
            sponsor=fake.company(),
            type=['A', 'B', 'N'][random.randint(0, 2)],
            start_time=fake.date_time_this_year(
                before_now=True,
                after_now=False,
                tzinfo=None
            ),
            end_time=fake.date_time_this_year(
                before_now=False,
                after_now=True,
                tzinfo=None
            ),
            details=fake.paragraph(
                nb_sentences=8,
                variable_nb_sentences=True,
                ext_word_list=None
            ),
            href=fake.url()
        )
        db.session.add(race)
        pass
    db.session.commit()
    pass


def fake_hot_race(count=10):
    for i in range(count):
        hot_race = HotRaceModel(
            name=fake.sentence(
                nb_words=8,
                variable_nb_words=True,
                ext_word_list=None
            ),
            sponsor=fake.company(),
            type=['A', 'B', 'N'][random.randint(0, 2)],
            start_time=fake.date_time_this_year(
                before_now=True,
                after_now=False,
                tzinfo=None
            ),
            end_time=fake.date_time_this_year(
                before_now=False,
                after_now=True,
                tzinfo=None
            ),
            details=fake.paragraph(
                nb_sentences=8,
                variable_nb_sentences=True,
                ext_word_list=None
            ),
            href=fake.url()
        )
        db.session.add(hot_race)
        pass
    db.session.commit()
    pass


def fake_news(count=60):
    for i in range(count):
        news = NewsModel(
            news_theme=fake.sentence(
                nb_words=8,
                variable_nb_words=True,
                ext_word_list=None
            ),
            news_content=fake.paragraph(
                nb_sentences=20,
                variable_nb_sentences=True,
                ext_word_list=None
            ),
            news_time=fake.date_time_this_decade(
                before_now=True,
                after_now=False,
                tzinfo=None
            ),
            race_info_id=random.randint(1, 40)
        )
        db.session.add(news)
        pass
    db.session.commit()
    pass


def fake_libs(count=100):
    for i in range(count):
        lib = LibsModel(
            name=fake.sentence(
                nb_words=8,
                variable_nb_words=True,
                ext_word_list=None
            ),
            type=['PPT', 'PPP', 'CQB'][random.randint(0, 2)],
            time=fake.date_time_this_year(
                before_now=False,
                after_now=True,
                tzinfo=None
            ),
            href=fake.url()
        )
        db.session.add(lib)
        pass
    db.session.commit()
    pass


def fake_exp(count=80):
    user_num = UserModel.query.count()
    hot_race_num = HotRaceModel.query.count()
    all_race_num = RaceModel.query.count()
    for i in range(count):
        exp = ExperienceModel(
            type=fake.sentence(
                nb_words=4,
                variable_nb_words=True,
                ext_word_list=None
            ),
            title=fake.sentence(
                nb_words=4,
                variable_nb_words=True,
                ext_word_list=None
            ),
            content=fake.paragraph(
                nb_sentences=20,
                variable_nb_sentences=True,
                ext_word_list=None
            ),
            time=fake.date_time_this_year(
                before_now=True,
                after_now=False,
                tzinfo=None
            ),
            author_id=random.randint(1, user_num),
            hot_race_id=random.randint(1, hot_race_num),
            all_race_id=random.randint(1, all_race_num)
        )
        db.session.add(exp)
        pass
    db.session.commit()
    pass


def fake_question(count=80):
    user_num = UserModel.query.count()
    for i in range(count):
        qst = QuestionModel(
            title=fake.sentence(
                nb_words=4,
                variable_nb_words=True,
                ext_word_list=None
            ),
            content=fake.paragraph(
                nb_sentences=20,
                variable_nb_sentences=True,
                ext_word_list=None
            ),
            create_time=fake.date_time_this_year(
                before_now=True,
                after_now=False,
                tzinfo=None
            ),
            view_num=random.randint(0, user_num),
            author_id=random.randint(1, user_num)
        )
        db.session.add(qst)
        pass
    db.session.commit()
    pass


def fake_answer(count=180):
    user_num = UserModel.query.count()
    qst_num = QuestionModel.query.count()
    for i in range(count):
        ans = AnswerModel(
            content=fake.paragraph(
                nb_sentences=20,
                variable_nb_sentences=True,
                ext_word_list=None
            ),
            create_time=fake.date_time_this_year(
                before_now=True,
                after_now=False,
                tzinfo=None
            ),
            question_id=random.randint(1, qst_num),
            author_id=random.randint(1, user_num)
        )
        db.session.add(ans)
        pass
    db.session.commit()
    pass

