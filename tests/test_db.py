import sqlite3

import pytest
from flaskr.db import get_db

def test_get_close_db(app):
    with app.app_context(): #context 생성
        db=get_db()
        assert db is get_db() #이 작업 이후, context가 끝나므로 db도 close

    with pytest.raises(sqlite3.ProgrammingError) as e:
        db.execute('SELECT 1') #db 연결이 끊겼으므로 실행되면 안됨

    assert 'closed' in str(e.value)

def test_init_db_command(runner,monkeypatch):
    class Recorder(object):
        called=False
    def fake_init_db():
        Recorder.called=True

    monkeypatch.setattr('flaskr.db.init_db',fake_init_db)
    result=runner.invoke(args=['init-db']) #cli command 등록되었으면 실행됨
    assert 'Initialized' in result.output
    assert Recorder.called