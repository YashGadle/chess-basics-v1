from typing import List, Tuple, TYPE_CHECKING
from ..utils.filter_out_pinned_moves import filter_out_pinned_moves

if TYPE_CHECKING:
    from board import Board
    from piece import Piece

def all_knight_moves(
    piece: 'Piece',
    board: 'Board',
    check_for_pin: bool = False
) -> List[Tuple[int, int]]:
    from board import Board
    moves: List[Tuple[int, int]] = []
    state = board.get_board_state()
    m, n = piece.position

    # All 8 possible knight moves
    knight_moves = [
        (m + 2, n + 1),
        (m + 2, n - 1),
        (m - 2, n + 1),
        (m - 2, n - 1),
        (m + 1, n + 2),
        (m + 1, n - 2),
        (m - 1, n + 2),
        (m - 1, n - 2),
    ]

    for x, y in knight_moves:
        if x < 0 or x >= Board.num_row or y < 0 or y >= Board.num_col:
            continue
        target_cell = state[x][y]

        if target_cell.piece is None:
            moves.append((x, y))
        elif target_cell.piece:
            if target_cell.piece.color != piece.color:
                moves.append((x, y))

    if check_for_pin:
        return filter_out_pinned_moves(piece, board, moves)

    return moves
