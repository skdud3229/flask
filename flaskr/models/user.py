from flaskr.db import db
from sqlalchemy import Integer,String
from sqlalchemy.orm import Mapped,mapped_column

from typing_extensions import Annotated

intpk=Annotated[int,mapped_column(primary_key=True,autoincrement="auto")]
required_name=Annotated[str,mapped_column(String(10),nullable=False,unique=True)]
pwd=Annotated[str,mapped_column(String(500),nullable=False)]

class User(db.Model):
    __tablename__="users"
    id:Mapped[intpk]
    username:Mapped[required_name]
    password:Mapped[pwd]

def get_user_by_username(username):
    user=User.query.filter_by(username=username).first()
    return user