import click
from flask.cli import with_appcontext
from app import db
from app.services.db_init import init_db

@click.command('init-db')
@with_appcontext
def init_db_command():
    """Comando para inicializar la base de datos con datos básicos"""
    init_db()
    click.echo('Base de datos inicializada.')

def register_commands(app):
    """Registrar comandos personalizados de Flask CLI"""
    app.cli.add_command(init_db_command)
