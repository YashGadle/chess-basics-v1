"""
Test the performance of the best genome produced by evolve-feedforward.py.
"""

import os
import pickle

import neat
import chess
import time

# load the winner
with open('winner-feedforward', 'rb') as f:
    c = pickle.load(f)

print('Loaded genome:')
print(c)

# Load the config file, which is assumed to live in
# the same directory as this script.
local_dir = os.path.dirname(__file__)
config_path = os.path.join(local_dir, 'config-feedforward')
config = neat.Config(neat.DefaultGenome, neat.DefaultReproduction,
                     neat.DefaultSpeciesSet, neat.DefaultStagnation,
                     config_path)

net = neat.nn.FeedForwardNetwork.create(c, config)

def board_to_nn_input(board: chess.Board):
    """
    6-bit piece type (one-hot) + 1-bit color per square = 7 bits × 64 = 448
    """
    piece_map = board.piece_map()
    inputs = []

    for square in chess.SQUARES:
        piece = piece_map.get(square)
        piece_encoding = [0] * 6
        color_bit = 0

        if piece:
            piece_encoding[piece.piece_type - 1] = 1  # 1-6 mapped to 0-5
            color_bit = 1 if piece.color == chess.WHITE else 0

        inputs.extend(piece_encoding)
        inputs.append(color_bit)

    return inputs  # length = 448

def decode_output(output):
    from_index = min(max(int(round(output[0] * 63)), 0), 63)
    to_index = min(max(int(round(output[1] * 63)), 0), 63)
    return from_index, to_index

def run_winner(winner_path="winner.pkl", config_path="config-feedforward.txt"):
    board = chess.Board()

    print("Starting game with best genome...\n")

    while not board.is_game_over():
        inputs = board_to_nn_input(board)
        output = net.activate(inputs)
        from_idx, to_idx = decode_output(output)

        move = chess.Move(from_idx, to_idx)

        if move in board.legal_moves:
            board.push(move)
            print(board.unicode(borders=True))
            print(f"Move played: {board.peek().uci()}\n")
        else:
            print(f"Illegal move attempted: {move.uci()}")
            break

        time.sleep(1)

    print("Game over:", board.result())

if __name__ == "__main__":
    run_winner()