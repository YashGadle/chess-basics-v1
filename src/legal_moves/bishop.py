from typing import List, Tuple, TYPE_CHECKING
from utils.filter_out_pinned_moves import filter_out_pinned_moves

if TYPE_CHECKING:
    from board import Board
    from piece import Piece

def all_bishop_moves(
    piece: 'Piece',
    board: 'Board',
    check_for_pin: bool = False
) -> List[Tuple[int, int]]:
    from board import Board
    moves: List[Tuple[int, int]] = []
    state = board.get_board_state()
    m, n = piece.position

    # Run through all 4 diagonals of the bishop
    i, j = m + 1, n + 1
    while i < Board.num_row and j < Board.num_col:
        if state[i][j].piece is None:
            moves.append((i, j))
        elif state[i][j].piece is not None:
            if state[i][j].piece.color != piece.color:
                moves.append((i, j))
                break
            else:
                break
        i += 1
        j += 1

    i, j = m - 1, n - 1
    while i >= 0 and j >= 0:
        if state[i][j].piece is None:
            moves.append((i, j))
        elif state[i][j].piece is not None:
            if state[i][j].piece.color != piece.color:
                moves.append((i, j))
                break
            else:
                break
        i -= 1
        j -= 1

    i, j = m + 1, n - 1
    while i < Board.num_row and j >= 0:
        if state[i][j].piece is None:
            moves.append((i, j))
        elif state[i][j].piece is not None:
            if state[i][j].piece.color != piece.color:
                moves.append((i, j))
                break
            else:
                break
        i += 1
        j -= 1

    i, j = m - 1, n + 1
    while i >= 0 and j < Board.num_col:
        if state[i][j].piece is None:
            moves.append((i, j))
        elif state[i][j].piece is not None:
            if state[i][j].piece.color != piece.color:
                moves.append((i, j))
                break
            else:
                break
        i -= 1
        j += 1

    if check_for_pin:
        return filter_out_pinned_moves(piece, board, moves)

    return moves
