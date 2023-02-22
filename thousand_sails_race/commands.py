
import click
from thousand_sails_race import app
from thousand_sails_race.models import *


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


@app.cli.command()
@click.option('--user', default=10, help='Quantity of users, default is 10.')
@click.option('--race', default=40, help='Quantity of races, default is 160.')
@click.option('--news', default=60, help='Quantity of news, default is 60.')
def forge(user, race, news):
    """Generate fake data"""

    from thousand_sails_race.fakes import fake_admin, fake_user, fake_race, fake_news

    db.drop_all()
    click.echo('Dropped tables.')
    db.create_all()
    click.echo('Initialized database.')

    click.echo('Generating the administrator...')
    fake_admin()
    click.echo('Generating %d users...' % user)
    fake_user()
    click.echo('Generating %d races info...' % race)
    fake_race()
    click.echo('Generating %d news info...' % news)
    fake_news()

