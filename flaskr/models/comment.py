from flaskr.db import db
from typing_extensions import Annotated,Optional
from sqlalchemy.orm import mapped_column,Mapped
from sqlalchemy import String,Integer,DateTime,func,select
from sqlalchemy.sql.functions import coalesce
from datetime import datetime


intpk=Annotated[int,mapped_column(primary_key=True,autoincrement="auto")]
str_100=Annotated[str,mapped_column(String(100),nullable=False)]
ref_id=Annotated[int,mapped_column(Integer,nullable=False)]
null_ref_id=Annotated[Optional[int],mapped_column(Integer,nullable=True)]
date_time=Annotated[datetime,mapped_column(DateTime(timezone=True),default=func.now(),nullable=False)]


class Comment(db.Model):
    id:Mapped[intpk]
    comment:Mapped[str_100]
    created_at:Mapped[date_time]
    writer:Mapped[ref_id]
    board_id:Mapped[ref_id]
    parent_id:Mapped[null_ref_id]

    @staticmethod
    def create_comment(comment,writer,board_id,parent_id):
        comment=Comment(comment=comment,writer=writer,board_id=board_id,parent_id=parent_id)
        db.session.add(comment)

    def update_comment(self,comment):
        self.comment=comment

    def delete_comment(self):
        db.session.delete(self)

    @classmethod
    def get_comment_by_id(cls,id):
        return db.session.execute(select(cls).where(cls.id==id)).first()
    
    @classmethod
    def get_comments_by_board(cls,board_id):
        query=select(cls.id,cls.parent_id,cls.comment,cls.writer,cls.created_at).where(cls.board_id==board_id).order_by(func.coalesce(cls.parent_id,cls.id),cls.created_at)
        return db.session.execute(query).all()
        
        
        

    
    

    


