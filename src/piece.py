from typing import List, Tuple, Optional, Literal
from .legal_moves.pawn import all_pawn_moves
from .legal_moves.queen import all_queen_moves
from .legal_moves.knight import all_knight_moves
from .legal_moves.rook import all_rook_moves
from .legal_moves.bishop import all_bishop_moves
from .legal_moves.king import all_king_moves

PieceColor = Literal["w", "b"]
PieceType = Literal["p", "r", "b", "n", "q", "k"]
Position = Tuple[int, int]
Promotion = Optional[Literal["r", "n", "b", "q"]]

class Piece:
    def __init__(self, type_: PieceType, color: PieceColor, position: Position):
        self.color = color
        self.type = type_
        self.position = position
        self.lost = False
        self.promotion: Promotion = None

    def get_legal_moves(self, board, check_for_pin: bool = False) -> List[Position]:
        if self.type == "p":
            return all_pawn_moves(self, board, check_for_pin)
        elif self.type == "q":
            return all_queen_moves(self, board, check_for_pin)
        elif self.type == "n":
            return all_knight_moves(self, board, check_for_pin)
        elif self.type == "r":
            return all_rook_moves(self, board, check_for_pin)
        elif self.type == "b":
            return all_bishop_moves(self, board, check_for_pin)
        elif self.type == "k":
            return all_king_moves(self, board)
        else:
            print("Piece type not implemented or not recognized.")
            return []

    def promote_pawn(self, new_type: Promotion):
        if self.type != "p":
            raise ValueError("Only pawns can be promoted")
        if new_type not in ["r", "n", "b", "q"]:
            raise ValueError("Invalid promotion type")
        self.type = new_type
        self.promotion = new_type

    def __repr__(self):
        return f"Piece(type={self.type}, color={self.color}, position={self.position}, lost={self.lost}, promotion={self.promotion})"
