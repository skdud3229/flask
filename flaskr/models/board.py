from flaskr.db import db
from sqlalchemy.orm import Mapped,mapped_column
from typing_extensions import Annotated,Optional
from sqlalchemy import String,DateTime,func,Column,Integer,desc
from datetime import datetime

intpk=Annotated[int,mapped_column(primary_key=True,autoincrement="auto")]
required_title=Annotated[str,mapped_column(String(100),nullable=False)]
required_contents=Annotated[str,mapped_column(String(5000),nullable=False)]
created_time=Annotated[datetime,mapped_column(DateTime(timezone=True),default=func.now(),nullable=False)]
updated_time=Annotated[Optional[datetime],mapped_column(DateTime(timezone=True),onupdate=func.now(),nullable=True)]
writer=Annotated[int,mapped_column(Integer)]


class Board(db.Model):
    __tablename__="boards"
    id: Mapped[intpk]
    title:Mapped[required_title]
    contents:Mapped[required_contents]
    writer:Mapped[writer]
    createdAt: Mapped[created_time]
    updatedAt: Mapped[updated_time]

def get_total_boards_num():
    return Board.query.count()

def get_boards(page,per_page):
    offset=(page-1)*per_page
    boards=Board.query.order_by(desc(Board.createdAt)).offset(offset).limit(per_page).all()
    return boards

def get_board_by_id(board_id):
    board=Board.query.filter_by(id=board_id).first()
    return board

def insert_board(title,contents,writer):
    board=Board(title=title,contents=contents,writer=writer)
    db.session.add(board)
    db.session.commit()

def update_board(title,contents,board):
    board.title=title
    board.contents=contents
    db.session.commit()

def delete_board(board):
    db.session.delete(board)
    db.session.commit()




    