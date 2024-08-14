import pytest
from flaskr.db import get_db

def test_index(auth,client):
    response=client.get('/')
    assert b"Log In" in response.data
    auth.login()
    response=client.get('/')
    assert b'test title' in response.data

@pytest.mark.parametrize('path',(
    '/create',
    '/1/update',
    '1/delete',
))
def test_login_required(client,path):
    response=client.post(path)
    assert response.headers['Location']=='/auth/login'

def test_author_required(app,client,auth):
    with app.app_context():
        db=get_db()
        db.execute('UPDATE post SET author_id = 2 WHERE id = 1')
        db.commit()

    auth.login()
    assert client.post('/1/update').status_code==403
    assert client.post('/1/delete').status_code == 403

    assert b'href="/1/update"' not in client.get('/').data

@pytest.mark.parametrize('path',(
    '/2/update',
    '/2/delete',
))
def test_exists_requred(client,auth,path):
    auth.login()
    assert client.post(path).status_code==404