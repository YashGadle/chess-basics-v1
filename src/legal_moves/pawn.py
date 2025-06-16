from typing import List, TYPE_CHECKING
from ..utils.filter_out_pinned_moves import filter_out_pinned_moves

if TYPE_CHECKING:
    from ..board import Board
    from ..piece import Piece

def all_pawn_moves(pawn: 'Piece', board: 'Board', check_for_pin: bool = False) -> list[tuple[int, int]]:
    from ..board import Board
    state = board.get_board_state()
    moves: list[tuple[int, int]] = []
    m, n = pawn.position

    white_pawn_moves: list[tuple[int, int, bool]] = [
        (m - 1, n, False),
        (m - 2, n, False),
        (m - 1, n - 1, True),
        (m - 1, n + 1, True),
    ]
    black_pawn_moves: list[tuple[int, int, bool]] = [
        (m + 1, n, False),
        (m + 2, n, False),
        (m + 1, n - 1, True),
        (m + 1, n + 1, True),
    ]
    pawn_moves = white_pawn_moves if pawn.color == "w" else black_pawn_moves

    for x, y, capture in pawn_moves:
        if x < 0 or x >= Board.num_row or y < 0 or y >= Board.num_col:
            continue
        target_cell = state[x][y]

        # Normal move
        if target_cell.piece is None and not capture:
            moves.append((x, y))
        elif (
            target_cell.piece is not None and
            target_cell.piece.color != pawn.color and
            capture
        ):
            # Capture move
            moves.append((x, y))

    if check_for_pin:
        return filter_out_pinned_moves(pawn, board, moves)

    return moves
