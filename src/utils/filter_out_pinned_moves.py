from typing import List, Tuple, TYPE_CHECKING
from legal_moves.king import is_in_check

if TYPE_CHECKING:
    from board import Board
    from piece import Piece

def filter_out_pinned_moves(
    piece: 'Piece',
    board: 'Board',
    moves: List[Tuple[int, int]]
) -> List[Tuple[int, int]]:
    m, n = piece.position

    valid_moves = []
    for x, y in moves:
        captured_piece = board.move_piece((m, n), (x, y), piece)  # Move the piece to the new position
        is_pinned = is_in_check(piece.color, board)  # Check if the king is in check after the move
        board.move_piece((x, y), (m, n), piece, captured_piece)  # Move back to original position
        if not is_pinned:
            valid_moves.append((x, y))
    return valid_moves
