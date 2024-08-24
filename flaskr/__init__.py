import os
from flask import Flask
from flask_jwt_extended import JWTManager
from flask_sqlalchemy import SQLAlchemy

def create_app(test_config=None):

    app=Flask(__name__,instance_relative_config=True)
    app.config.from_mapping(
        SECRET_KEY='dev',
        DATABASE=os.path.join(app.instance_path,'flaskr.sqlite'),
    )

    if test_config is None:
        app.config.from_pyfile('config.py')
    else:
        app.config.from_mapping(test_config)

    try:
        os.makedirs(app.instance_path)
    except OSError:
        pass

    @app.route('/hello')
    def hello():
        return 'Hello, World!'
    
    jwt=JWTManager(app) #JWTManager가 app을 관리하도록

    from flaskr.db import db,init_cli
    init_cli(app)
    db.init_app(app)
    

    from . import auth
    app.register_blueprint(auth.bp)

    from . import blog
    from .models.board import Board
    from .services.board_service import BoardService
    board_service = BoardService(Board)
    board_view = blog.BoardView.as_view('board_view', board_service)
    blog.bp.add_url_rule('/', view_func=board_view, methods=['GET','POST'])
    blog.bp.add_url_rule('/<int:page_num>', view_func=board_view, methods=['GET'])
    blog.bp.add_url_rule('/<int:board_id>', view_func=board_view, methods=['PUT','DELETE'])
    app.register_blueprint(blog.bp)
    
    return app


    