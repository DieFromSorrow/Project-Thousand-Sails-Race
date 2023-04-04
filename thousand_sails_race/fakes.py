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


def fake_user(count=100):
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
    db.session.commit()


def fake_race(count=160):
    for i in range(count):
        race = RaceinfoModel(
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
    db.session.commit()


def fake_hot_race(count=10):
    for i in range(count):
        hot_race = HotraceinfoModel(
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
    db.session.commit()


def fake_news(count=60):
    for i in range(count):
        news = NewsinfoModel(
            newstheme=fake.sentence(
                nb_words=8,
                variable_nb_words=True,
                ext_word_list=None
            ),
            newscontent=fake.paragraph(
                nb_sentences=20,
                variable_nb_sentences=True,
                ext_word_list=None
            ),
            news_time=fake.date_time_this_decade(
                before_now=True,
                after_now=False,
                tzinfo=None
            ),
            raceinfo_id=random.randint(1, 40)
        )
        db.session.add(news)
    db.session.commit()


def fake_libs(count=100):
    for i in range(count):
        lib = LibsinfoModel(
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
    db.session.commit()

