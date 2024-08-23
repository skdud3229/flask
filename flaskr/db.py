from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import DeclarativeBase
import click
from flask import current_app


class Base(DeclarativeBase):
    pass

db=SQLAlchemy(model_class=Base)

@click.command('init-db')
def init_db_command():
    db.drop_all()
    db.create_all()
    click.echo('Initialized the database.')
    

def init_cli(app):
    app.cli.add_command(init_db_command)

# import sqlite3

# import click
# from flask import current_app,g

# #connection is tied to request, created when handling a request, then closed before the response is sent
# def get_db():
#     if 'db' not in g: #g는 각 request에 대해 unique하며, 한 request가 여러 번 db를 호출하면 기존의 connection을 재사용  
#         g.db=sqlite3.connect(
#             current_app.config['DATABASE'],
#             detect_types=sqlite3.PARSE_DECLTYPES
#         )
#         g.db.row_factory=sqlite3.Row #rows를 반환할 것임을 나타냄
#     return g.db

# def close_db(e=None):
#     db=g.pop('db',None)
#     if db is not None:
#         db.close()

# def init_db():
#     db=get_db()
#     with current_app.open_resource('schema.sql') as f: #현재 package 내부의 schema.sql 열기
#         db.executescript(f.read().decode('utf8'))

# @click.command('init-db')
# def init_db_command():
#     init_db()
#     click.echo('Initialized the database.')

# def init_app(app):
#     app.teardown_appcontext(close_db) #response를 반환하고 clean up
#     app.cli.add_command(init_db_command)