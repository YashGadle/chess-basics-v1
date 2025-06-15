from typing import List, Optional, Tuple
import sys

from piece import Piece, Position
from utils.coordinates_to_notations import coordinates_to_notations
from utils.parse_fen import parse_fen, ParsedFEN
from utils.default_board_state import make_default_state

Position = Tuple[int, int]

class Cell:
  def __init__(self, piece: Optional[Piece], color: str):
    self.piece = piece
    self.color = color  # 'w' or 'b'
    
  def render_cell_node(self) -> str:
    if self.piece is None:
      return "."
    else:
      return self.piece.type

class Board:
  num_row = 8
  num_col = 8

  def __init__(self, parsed_board: Optional[ParsedFEN] = None):
    if parsed_board:
      self.state: List[List[Cell]] = []
      for row_index, row in enumerate(parsed_board['board']):
        board_row = []
        for col_index, cell in enumerate(row):
          color = "w" if (row_index + col_index) % 2 == 0 else "b"
          if cell == "":
            board_row.append(Cell(None, color))
          elif cell.islower():
            piece = Piece(cell, "b", (row_index, col_index))
            board_row.append(Cell(piece, color))
          else:
            piece = Piece(cell.lower(), "w", (row_index, col_index))
            board_row.append(Cell(piece, color))
        self.state.append(board_row)
    else:
      self.state = make_default_state()

  def get_board_state(self) -> List[List[Cell]]:
    return self.state

  def render_board(self):
    for i in range(Board.num_row):
      row_repr = []
      for j in range(Board.num_col):
        cell = self.state[i][j]
        row_repr.append(cell.render_cell_node())
      print(" | ".join(row_repr))

  def move_piece(
    self,
    from_pos: Position,
    to_pos: Position,
    piece: Piece,
    original_piece: Optional[Piece] = None
  ) -> Optional[Piece]:
    from_row, from_col = from_pos
    to_row, to_col = to_pos

    if (
      from_row < 0 or from_row >= Board.num_row or
      from_col < 0 or from_col >= Board.num_col or
      to_row < 0 or to_row >= Board.num_row or
      to_col < 0 or to_col >= Board.num_col
    ):
      print("Invalid move")
      return None

    captured_piece = self.state[to_row][to_col].piece
    self.state[to_row][to_col].piece = piece
    self.state[from_row][from_col].piece = original_piece
    return captured_piece

def setup_chess_board(board: Board):
  board.render_board()

# Example usage:
if __name__ == "__main__":
  import urllib.parse

  # Simulate getting FEN from URL
  fen = None
  if len(sys.argv) > 1:
    params = urllib.parse.parse_qs(sys.argv[1])
    fen = params.get("fen", [None])[0]

  parsed_fen = parse_fen(fen) if fen else None

  board = Board(parsed_fen)
  setup_chess_board(board)
