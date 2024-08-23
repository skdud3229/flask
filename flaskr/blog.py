from flask import (
    Blueprint,request,g,abort,jsonify
)

from flaskr.auth import login_required
from flaskr.models.board import *
from math import ceil


bp=Blueprint('blog',__name__)
boards_per_page=10

@bp.get('/', defaults={'page_num': 1})
@bp.get('/<int:page_num>')
def index(page_num):
    #limit과 offset 방식
    total_count=get_total_boards_num()
    total_pages=ceil(total_count/boards_per_page)
    if page_num<1:  
        page_num=1
    elif total_pages<page_num: 
        page_num=total_pages

    boards=get_boards(page_num,boards_per_page)
    board_list= [{
            'id': board.id,
            'title': board.title,
            'contents': board.contents,
            'createdAt': board.createdAt.isoformat(),
            'updatedAt': board.updatedAt.isoformat() if board.updatedAt else None}
            for board in boards
            ]
    return jsonify({
        'page':page_num,
        'per_page':boards_per_page,
        'total_items':total_count,
        'total_pages':total_pages,
        'boards':board_list,
        })

    #추후 인덱스/커버링 인덱스 방식을 사용하도록 수정

@bp.post('/create')
@login_required
def create():
    body=request.get_json()
    insert_board(title=body['title'],contents=body['contents'],writer=g.user)
    return '성공'

@bp.post('/update/<int:board_id>')
@login_required
def update(board_id):
    board=get_board_by_id(board_id)
    if(board==None):
        abort(404,'해당 게시글이 존재하지 않습니다.')
    if board.writer!=g.user:
        abort(400,'해당 게시글 수정 권한이 없습니다.')
    body=request.get_json()
    update_board(title=body['title'],contents=body['contents'],board=board)
    
    return '성공'

@bp.post('/delete/<int:board_id>')
@login_required
def delete(board_id):
    board=get_board_by_id(board_id)
    if(board==None):
        abort(404,'해당 게시글이 존재하지 않습니다.')
    if board.writer!=g.user:
        abort(400,'해당 게시글 수정 권한이 없습니다.')
    delete_board(board)
    return '성공'
    






# from flask import(
#     Blueprint,flash,g,redirect,render_template,request,url_for
# )

# from werkzeug.exceptions import abort

# from flaskr.auth import login_required
# from flaskr.db import get_db

# bp=Blueprint('blog',__name__)

# @bp.route('/')
# def index():
#     db=get_db()
#     posts=db.execute(
#         'SELECT p.id, title, body, created, author_id, username'
#         ' FROM post p JOIN user u ON p.author_id=u.id'
#         ' ORDER BY created DESC'
#     ).fetchall()
#     return render_template('blog/index.html',posts=posts)

# @bp.route('/create',methods=('GET','POST'))
# @login_required
# def create():
#     if request.method=='POST':
#             title=request.form['title']
#             body=request.form['body']
#             error=None

#             if not title:
#                 error='Title is required.'

#             if error is not None:
#                 flash(error)
#             else:
#                 db=get_db()
#                 db.execute(
#                     'INSERT INTO post (title, body, author_id)'
#                     ' VALUES (?, ?, ?)',(title, body, g.user['id'])
#                 )
#                 db.commit()
#                 return redirect(url_for('blog.index'))
#     return render_template('blog/create.html')

# def get_post(id,check_author=True):
#     post=get_db().execute(
#         'SELECT p.id, title, body, created, author_id, username'
#         ' FROM post p JOIN user u ON p.author_id = u.id'
#         ' WHERE p.id = ?',
#         (id,)
#     ).fetchone()
#     if post is None:
#          abort(404,f"Post id {id} doesn't exist.")
#     if check_author and post['author_id']!=g.user['id']:
#          abort(403)
#     return post

# @bp.route('/<int:id>/update',methods=('GET','POST'))
# @login_required
# def update(id):
#     post=get_post(id)
#     if request.method=='POST':
#         title = request.form['title']
#         body = request.form['body']
#         error = None

#         if not title:
#             error = 'Title is required.'

#         if error is not None:
#             flash(error)
#         else:
#             db = get_db()
#             db.execute(
#                 'UPDATE post SET title = ?, body = ?'
#                 ' WHERE id = ?',
#                 (title, body, id)
#             )
#             db.commit()
#             return redirect(url_for('blog.index'))

#     return render_template('blog/update.html', post=post)

# @bp.route('/<int:id>/delete',methods=('POST',))
# @login_required
# def delete(id):
#     get_post(id)
#     db=get_db()
#     db.execute('DELETE FROM post WHERE id=?',(id,))
#     db.commit()
#     return redirect(url_for('blog.index'))


            