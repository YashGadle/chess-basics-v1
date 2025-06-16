from typing import TYPE_CHECKING
from .bishop import all_bishop_moves
from .rook import all_rook_moves

if TYPE_CHECKING:
    from ..board import Board
    from ..piece import Piece

def all_queen_moves(piece: 'Piece', board: 'Board', check_for_pin: bool = False) -> list[tuple[int, int]]:
    rook_moves = all_rook_moves(piece, board, check_for_pin)
    bishop_moves = all_bishop_moves(piece, board, check_for_pin)
    moves = rook_moves + bishop_moves
    return moves
