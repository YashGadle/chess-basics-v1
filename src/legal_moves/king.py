from typing import List, Tuple, TYPE_CHECKING

if TYPE_CHECKING:
    from board import Board 
    from piece import Piece

def all_king_moves(piece: 'Piece', board: 'Board') -> List[Tuple[int, int]]:
    from ..utils.filter_out_pinned_moves import filter_out_pinned_moves
    from ..board import Board
    m, n = piece.position
    moves: List[Tuple[int, int]] = []
    king_moves = [
        (m + 1, n),     # down
        (m - 1, n),     # up
        (m, n + 1),     # right
        (m, n - 1),     # left
        (m + 1, n + 1), # down-right
        (m + 1, n - 1), # down-left
        (m - 1, n + 1), # up-right
        (m - 1, n - 1), # up-left
    ]

    state = board.get_board_state()

    for x, y in king_moves:
        if x < 0 or x >= Board.num_row or y < 0 or y >= Board.num_col:
            continue
        target_cell = state[x][y]
        if target_cell.piece is None or target_cell.piece.color != piece.color:
            moves.append((x, y))

    return filter_out_pinned_moves(piece, board, moves)

def is_in_check(color: str, board: 'Board') -> bool:
    king_x, king_y = get_king_position(board, color)
    state = board.get_board_state()
    king_cell = state[king_x][king_y]
    opponent_color = "b" if king_cell.piece and king_cell.piece.color == "w" else "w"
    opponent_pieces = [
        cell.piece
        for row in state
        for cell in row
        if cell.piece and cell.piece.color == opponent_color
    ]
    for piece in opponent_pieces:
        if not piece:
            continue
        legal_moves = piece.get_legal_moves(board, check_for_pin=False)
        if any(move[0] == king_x and move[1] == king_y for move in legal_moves):
            return True
    return False

def get_king_position(board: 'Board', color: str) -> Tuple[int, int]:
    from ..board import Board
    for i in range(Board.num_row):
        for j in range(Board.num_col):
            cell = board.get_board_state()[i][j]
            if cell.piece and cell.piece.type == "k" and cell.piece.color == color:
                return (i, j)
    raise Exception(f"King of color {color} not found on the board.",)
