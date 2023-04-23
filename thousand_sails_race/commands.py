import click
from thousand_sails_race.models import *


def register_initdb(app):
    @app.cli.command()
    @click.option('--drop', is_flag=True, help='Create after drop')
    def initdb(drop):
        """Initialize the database"""
        if drop:
            click.confirm('This operation will delete the database, do you want to continue?', abort=True)
            db.drop_all()
            click.echo('Dropped tables.')
        db.create_all()
        click.echo('Initialized database.')
        pass


def register_forge(app):
    @app.cli.command()
    @click.option('--user', default=30, help='Quantity of users, default is 30.')
    @click.option('--race', default=160, help='Quantity of races, default is 160.')
    @click.option('--news', default=60, help='Quantity of news, default is 60.')
    @click.option('--lib', default=100, help='Quantity of library, default is 100.')
    @click.option('--hot_race', default=10, help='Quantity of hot_races, default is 10')
    @click.option('--exp', default=50, help='Quantity of experiences, default is 50')
    @click.option('--qst', default=80, help='Quantity of questions, default is 80')
    @click.option('--ans', default=180, help='Quantity of answers, default is 180')
    def forge(user, race, news, lib, hot_race, exp, qst, ans):
        """Generate fake data"""

        from thousand_sails_race.fakes \
            import fake_admin, fake_user, fake_race, fake_news, fake_libs, \
            fake_hot_race, fake_exp, fake_question, fake_answer

        db.drop_all()
        click.echo('Dropped tables.')
        db.create_all()
        click.echo('Initialized database.')

        click.echo('Generating the administrator...')
        fake_admin()
        click.echo('Generating %d users...' % user)
        fake_user(user)
        click.echo('Generating %d races info...' % race)
        fake_race(race)
        click.echo('Generating %d news info...' % news)
        fake_news(news)
        click.echo('Generating %d libs info...' % lib)
        fake_libs(lib)
        click.echo('Generating %d hot_race info...' % hot_race)
        fake_hot_race(hot_race)
        click.echo('Generating %d experiences info' % exp)
        fake_exp(exp)
        click.echo('Generating %d questions info' % qst)
        fake_question(qst)
        click.echo('Generating %d answers info' % ans)
        fake_answer(ans)

        click.echo('done.')
        pass
