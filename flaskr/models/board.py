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

    @classmethod
    def get_total_boards_num(cls):
        return cls.query.count()

    @classmethod
    def get_boards(cls,page,per_page):
        offset=(page-1)*per_page
        return cls.query.order_by(desc(cls.createdAt)).offset(offset).limit(per_page).all()
    
    @classmethod
    def get_board_by_id(cls,board_id):
        return cls.query.filter_by(id=board_id).first()

    @staticmethod
    def create_board(title,contents,writer):
        board=Board(title=title,contents=contents,writer=writer)
        db.session.add(board)

    def update_board(self,title,contents):
        self.title=title
        self.contents=contents

    def delete_board(self):
        db.session.delete(self)




    