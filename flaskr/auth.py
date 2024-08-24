import functools
from flask import(
    Blueprint,redirect,request,url_for,make_response,abort,jsonify,g
)
from werkzeug.security import check_password_hash,generate_password_hash
from flask_jwt_extended import (
    create_access_token,create_refresh_token,set_refresh_cookies,verify_jwt_in_request,get_jwt_identity
)
from flaskr.db import db
from flaskr.models import user as u
from sqlalchemy.exc import IntegrityError

bp=Blueprint('auth',__name__,url_prefix='/auth')

@bp.post('/register')
def register():
    username=request.form['username']
    password=request.form['password']
    print(password)

    error=None

    if not username:
        abort(400,'입력한 회원명이 없습니다.')
    elif not password:
        abort(400,'입력한 비밀번호가 없습니다.')

    if error is None:
        try:
            user=u.User(username=username,password=generate_password_hash(password))
            db.session.add(user)
            db.session.commit()
        except  IntegrityError:
            db.session.rollback()
            abort(409,'이미 등록된 회원명입니다.')
        else:
            return jsonify("회원가입 성공했습니다.")

@bp.post('/login')
def login():
    username=request.form['username']
    password=request.form['password']

    error=None

    user=u.get_user_by_username(username)
    
    if user is None:
        abort(400,'해당 회원이 존재하지 않습니다.')
    elif not check_password_hash(user.password,password):
        abort(400,'비밀 번호가 틀렸습니다.')

    elif error is None:
        response=make_response()
        userid=user.id
        access_token=create_access_token(identity=userid)
        refresh_token=create_refresh_token(identity=userid)
        response.headers['Authorization']='Bearer '+access_token
        set_refresh_cookies(response,refresh_token)
        return response
        
@bp.post('/logout')
def logout():
    #이후에 redis랑 연동했을 때 refresh token 만료시키기
    return  redirect(url_for('index'))

@bp.post('/refresh')
def refresh_access_Token():
    verify_jwt_in_request(refresh=True)
    identity=get_jwt_identity()
    response=make_response()
    access_token=create_access_token(identity=identity)
    refresh_token=create_refresh_token(identity=identity)
    response.headers['Authorization']='Bearer '+access_token
    set_refresh_cookies(response,refresh_token)
    return response

def login_required(view):
    @functools.wraps(view) #view를 wrap하는 새로운 view function을 만듦
    def wrapped_view(*args,**kwargs):
        try:
            verify_jwt_in_request()
            g.user=get_jwt_identity()
            return view(*args,**kwargs)
        except Exception as e:
            abort(401, '인증 오류 발생: {}'.format(str(e)))
    return wrapped_view

@bp.route('/protected',methods=['GET','POST'])
@login_required
def refresh_access_token():
    return jsonify('성공')




