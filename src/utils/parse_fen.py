from typing import List, Optional, TypedDict

class CastlingRights(TypedDict):
  whiteKingSide: bool
  whiteQueenSide: bool
  blackKingSide: bool
  blackQueenSide: bool

class EnPassantTarget(TypedDict):
  row: int
  col: int
  square: str

class ParsedFEN(TypedDict):
  board: List[List[str]]
  activeColor: str
  castlingRights: CastlingRights
  enPassantTarget: Optional[EnPassantTarget]
  halfmoveClock: int
  fullmoveNumber: int

def parse_fen(fen: str) -> ParsedFEN:
  piece_placement, active_color, castling_str, en_passant_str, halfmove_clock, fullmove_number = fen.split(" ")

  # Parse board layout
  board = []
  for rank in piece_placement.split("/"):
    row = []
    for char in rank:
      if not char.isdigit():
        row.append(char)
      else:
        row.extend([""] * int(char))
    board.append(row)

  # Castling rights
  castling_rights: CastlingRights = {
    "whiteKingSide": "K" in castling_str,
    "whiteQueenSide": "Q" in castling_str,
    "blackKingSide": "k" in castling_str,
    "blackQueenSide": "q" in castling_str,
  }

  # En passant target square
  en_passant_target: Optional[EnPassantTarget] = None
  if en_passant_str != "-":
    file = en_passant_str[0]
    rank = en_passant_str[1]
    col = ord(file) - ord("a")
    row = 8 - int(rank)
    en_passant_target = {"row": row, "col": col, "square": en_passant_str}

  return {
    "board": board,
    "activeColor": active_color,
    "castlingRights": castling_rights,
    "enPassantTarget": en_passant_target,
    "halfmoveClock": int(halfmove_clock),
    "fullmoveNumber": int(fullmove_number),
  }