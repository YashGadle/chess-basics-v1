from typing import List, Optional, Tuple
import sys

from .piece import Piece, Position
from .utils.coordinates_to_notations import coordinates_to_notations
from .utils.parse_fen import parse_fen, ParsedFEN
from .utils.default_board_state import make_default_state
from .utils.decompress_nn_output import decompress_nn_output

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

  def __init__(self, fen: str, parsed_board: Optional[ParsedFEN] = None):
    self.num_tries = 0
    self.fen = fen
    self.parsed_fen = parsed_board
    if parsed_board:
      self.state: List[List[Cell]] = []
      for row_index, row in enumerate(parsed_board['board']):
        board_row = []
        for col_index, cell in enumerate(row):
          square_color = "w" if (row_index + col_index) % 2 == 0 else "b"
          if cell == "":
            board_row.append(Cell(None, square_color))
          else:
            color = "w" if cell.isupper() else "b"
            piece_type = cell.lower()
            piece = Piece(piece_type, color, (row_index, col_index))
            board_row.append(Cell(piece, square_color))
        self.state.append(board_row)
    else:
      self.state = make_default_state()

  def get_board_state(self) -> List[List[Cell]]:
    return self.state
  
  def board_to_nn_input(self) -> list[int]:
    """
    Converts a 8x8 board (List[List[Cell]]) into a 448-bit input vector.
    Each cell becomes 8 bits:
        - 6-bit one-hot for piece type: P, N, B, R, Q, K
        - 1-bit for color (0 = white, 1 = black)
    """
    piece_encoding = {
        "P": [1, 0, 0, 0, 0, 0],
        "N": [0, 1, 0, 0, 0, 0],
        "B": [0, 0, 1, 0, 0, 0],
        "R": [0, 0, 0, 1, 0, 0],
        "Q": [0, 0, 0, 0, 1, 0],
        "K": [0, 0, 0, 0, 0, 1]
    }

    input_vector = []

    for row in self.state:
        for cell in row:
            if cell.piece is None:
                input_vector.extend([0]*7)  # Empty square
            else:
                # 6-bit one-hot
                piece_bits = piece_encoding.get(cell.piece.type.upper(), [0]*6)
                # 1-bit color
                color_bit = 0 if cell.piece.color == "white" else 1

                input_vector.extend(piece_bits + [color_bit])

    return input_vector
  
  def get_board_state_nn(self) -> List[List[Optional[str]]]:
    board_state = []
    for row in self.state:
      board_row = []
      for cell in row:
        if cell.piece is None:
          board_row.append(None)
        else:
          board_row.append(coordinates_to_notations(cell.piece.type, cell.piece.color))
      board_state.append(board_row)
    return board_state

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
      return None

    captured_piece = self.state[to_row][to_col].piece
    self.state[to_row][to_col].piece = piece
    self.state[from_row][from_col].piece = original_piece
    return captured_piece
  
  def move_piece_nn(self, from_square: float, to_square: float) -> Optional[Piece]:
    (from_row, from_col), (to_row, to_col) = decompress_nn_output(from_square, to_square)
    if not (0 <= from_row < Board.num_row and 0 <= from_col < Board.num_col and
            0 <= to_row < Board.num_row and 0 <= to_col < Board.num_col):
      return None

    piece = self.state[from_row][from_col].piece
    if piece is None:
      return None
    
    return self.move_piece((from_row, from_col), (to_row, to_col), piece)
    
  def calculate_fitness(self, from_square: float, to_square: float) -> int:
    (from_row, from_col), (to_row, to_col) = decompress_nn_output(from_square, to_square)
    if not (0 <= from_row < Board.num_row and 0 <= from_col < Board.num_col and
            0 <= to_row < Board.num_row and 0 <= to_col < Board.num_col):
      return -1
    piece = self.state[from_row][from_col].piece

    if piece is None:
      # No piece to move
      return -0.5
    legal_moves = piece.get_legal_moves(self, check_for_pin=True)
    if (to_row, to_col) not in legal_moves:
      # no legal moves, but was able to find a piece
      return 0
    if self.state[to_row][to_col].piece is None:
      # Moving to an empty square
      return 1
    elif self.state[to_row][to_col].piece.color != piece.color:
      # Capturing an opponent's piece
      return 2
    return 0

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
