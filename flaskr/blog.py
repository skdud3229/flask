from flask import Blueprint, request, g, jsonify, abort
from flask.views import MethodView
from flaskr.services.board_service import BoardService, BoardNotFoundError, PermissionDeniedError
from flaskr.models.board import Board
from flaskr.auth import login_required

bp = Blueprint('blog', __name__)
class BoardView(MethodView):
    def __init__(self, board_service,comment_service):
        self.board_service = board_service
        self.comment_service = comment_service

    def get(self, board_id=None):
        if board_id==None:
            page_num=request.args.get('pagenum',1,type=int)
            boards_per_page=5
            page_num, total_count, total_pages, boards = self.board_service.fetch_boards(page_num, boards_per_page)
            board_list = [{
                'id': board.id,
                'title': board.title,
                'contents': board.contents,
                'createdAt': board.createdAt.isoformat(),
                'updatedAt': board.updatedAt.isoformat() if board.updatedAt else None
            } for board in boards]
            return jsonify({
            'page': page_num,
            'per_page': boards_per_page,
            'total_items': total_count,
            'total_pages': total_pages,
            'boards': board_list,
            })

     
        else:
            board=self.board_service.get_board_by_id(board_id)
            board_data={
                'id': board.id,
                'title': board.title,
                'contents': board.contents,
                'createdAt': board.createdAt.isoformat(),
                'updatedAt': board.updatedAt.isoformat() if board.updatedAt else None
            } 
            
            comments=self.comment_service.get_comments_by_board(board_id=board_id)
            comment_list=[{
                    'id':comment.id,
                    'comments':comment.comment,
                    'isreply': 0 if comment.parent_id==None else 1,
                    'createdAt':comment.created_at.isoformat()
                    }for comment in comments]
            return jsonify({
                'board': board_data,
                'comments':comment_list
            })


    

    
    @login_required
    def post(self):
        body = request.get_json()
        try:
            self.board_service.create_board(title=body['title'], contents=body['contents'], writer=g.user)
        except Exception as e:
            abort(500, str(e))  # Handle unexpected errors
        return 'Success', 201

    @login_required
    def put(self, board_id):
        body = request.get_json()
        try:
            self.board_service.modify_board(board_id, title=body['title'], contents=body['contents'], writer=g.user)
        except BoardNotFoundError:
            abort(404, 'Board not found')
        except PermissionDeniedError:
            abort(403, 'Permission denied')
        return 'Success', 200

    @login_required
    def delete(self, board_id):
        try:
            self.board_service.remove_board(board_id, writer=g.user)
        except BoardNotFoundError:
            abort(404, 'Board not found')
        except PermissionDeniedError:
            abort(403, 'Permission denied')
        return 'Success', 200

