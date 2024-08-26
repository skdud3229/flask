from flask import Blueprint, request, g, jsonify, abort
from flask.views import MethodView
from flaskr.models.board import Board
from flaskr.auth import login_required

bp = Blueprint('comment', __name__)
class CommentView(MethodView):
    def __init__(self, comment_service):
        self.comment_service = comment_service
    
    @login_required
    def post(self):
        body = request.get_json()
        try:
            self.comment_service.create_comment(comment=body['comment'], writer=g.user,board_id=body['board_id'],parent_id=body['parent_id'])
        except Exception as e:
            abort(500, str(e))  # Handle unexpected errors
        return 'Success', 201

