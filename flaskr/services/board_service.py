from .transaction import transaction

class BoardService:
    def __init__(self, board_dao):
        self.board_dao = board_dao

    def fetch_boards(self, page_num, per_page):
        total_count = self.board_dao.get_total_boards_num()
        total_pages = (total_count + per_page - 1) // per_page
        if page_num < 1:
            page_num = 1
        elif page_num > total_pages:
            page_num = total_pages

        boards = self.board_dao.get_boards(page_num, per_page)
        return page_num, total_count, total_pages, boards

    def create_board(self, title, contents, writer):
        with transaction():
            return self.board_dao.create_board(title, contents, writer)

    def modify_board(self, board_id, title, contents, writer):
        board = self.board_dao.get_board_by_id(board_id)
        if board is None:
            raise BoardNotFoundError("Board not found")
        if board.writer != writer:
            raise PermissionDeniedError("Permission denied")
        with transaction():
            board.update_board(title, contents)

    def remove_board(self, board_id, writer):
        board = self.board_dao.get_board_by_id(board_id)
        if board is None:
            raise BoardNotFoundError("Board not found")
        if board.writer != writer:
            raise PermissionDeniedError("Permission denied")
        with transaction():
            board.delete_board()

class BoardNotFoundError(Exception):
    pass

class PermissionDeniedError(Exception):
    pass
