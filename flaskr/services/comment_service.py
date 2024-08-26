from .transaction import transaction
class CommentService:
    def __init__(self,comment_dao):
        self.comment_dao=comment_dao

    def create_comment(self,comment,writer,board_id,parent_id):
        with transaction():
            self.comment_dao.create_comment(comment=comment,writer=writer,board_id=board_id,parent_id=parent_id)

    def update_comment(self,comment):
        with transaction():
            self.comment_dao.update_comment(comment=comment)

    def delete_comment(self):
        with transaction():
            self.comment_dao.delete_comment()
    
    def get_comments_by_board(self,board_id):
        return self.comment_dao.get_comments_by_board(board_id)
