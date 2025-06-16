import chess
import random

def is_valid_fen(board: chess.Board) -> bool:
    # Check both kings are present
    if not board.king(chess.WHITE) or not board.king(chess.BLACK):
        return False

    # Check no pawns on 1st or 8th rank
    for square in board.pieces(chess.PAWN, chess.WHITE) | board.pieces(chess.PAWN, chess.BLACK):
        rank = chess.square_rank(square)
        if rank == 0 or rank == 7:
            return False

    return True

def generate_random_legal_fens(num_positions=100, max_moves=10):
    fens = set()
    fens.add(chess.Board().fen())  # Always include standard starting position

    while len(fens) < num_positions:
        board = chess.Board()
        for _ in range(random.randint(1, max_moves)):
            if board.is_game_over():
                break
            move = random.choice(list(board.legal_moves))
            board.push(move)

        if board.is_game_over():
            continue

        if not is_valid_fen(board):
            continue

        fens.add(board.fen())

    return list(fens)

if __name__ == "__main__":
    fens = generate_random_legal_fens(num_positions=100)
    with open("random_fens.txt", "w") as f:
        for fen in fens:
            f.write("\"" + fen + "\"," + "\n")