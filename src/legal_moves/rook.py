from typing import List, Tuple, TYPE_CHECKING
from ..utils.filter_out_pinned_moves import filter_out_pinned_moves

if TYPE_CHECKING:
    from board import Board
    from piece import Piece

def all_rook_moves(
    piece: 'Piece',
    board: 'Board',
    check_for_pin: bool = False
) -> List[Tuple[int, int]]:
    from board import Board
    moves: List[Tuple[int, int]] = []
    state = board.get_board_state()
    m, n = piece.position

    # Run through all vertical and horizontal directions
    # Down
    i, j = m + 1, n
    while i < Board.num_row:
        target_cell = state[i][j]
        if target_cell.piece is None:
            moves.append((i, j))
        elif target_cell.piece:
            if target_cell.piece.color != piece.color:
                moves.append((i, j))
                break
            else:
                break
        i += 1

    # Up
    i, j = m - 1, n
    while i >= 0:
        target_cell = state[i][j]
        if target_cell.piece is None:
            moves.append((i, j))
        elif target_cell.piece:
            if target_cell.piece.color != piece.color:
                moves.append((i, j))
                break
            else:
                break
        i -= 1

    # Right
    i, j = m, n + 1
    while j < Board.num_col:
        target_cell = state[i][j]
        if target_cell.piece is None:
            moves.append((i, j))
        elif target_cell.piece:
            if target_cell.piece.color != piece.color:
                moves.append((i, j))
                break
            else:
                break
        j += 1

    # Left
    i, j = m, n - 1
    while j >= 0:
        target_cell = state[i][j]
        if target_cell.piece is None:
            moves.append((i, j))
        elif target_cell.piece:
            if target_cell.piece.color != piece.color:
                moves.append((i, j))
                break
            else:
                break
        j -= 1

    if check_for_pin:
        return filter_out_pinned_moves(piece, board, moves)

    return moves