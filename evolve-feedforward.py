"""
Single-pole balancing experiment using a feed-forward neural network.
"""

from typing import List
import multiprocessing
import os
import pickle

from src.utils import random_fens
import neat
import visualize
import chess
import random


runs_per_net = 5

def fen_to_nn_input(board: chess.Board) -> List[int]:
    piece_encoding = {
        'p': [0,0,0,0,0,1],
        'n': [0,0,0,0,1,0],
        'b': [0,0,0,1,0,0],
        'r': [0,0,1,0,0,0],
        'q': [0,1,0,0,0,0],
        'k': [1,0,0,0,0,0],
    }

    input_vector = []
    for square in chess.SQUARES:
        piece = board.piece_at(square)
        if piece is None:
            input_vector.extend([0]*7)
        else:
            bits = piece_encoding[piece.symbol().lower()]
            color_bit = [0] if piece.color == chess.WHITE else [1]
            input_vector.extend(bits + color_bit)

    return input_vector

def decompress_nn_output(from_square, to_square):
    from_index = min(max(int(from_square * 63), 0), 63)
    to_index = min(max(int(to_square * 63), 0), 63)
    return from_index, to_index

# Use the NN network phenotype and the discrete actuator force function.
def eval_genome(genome, config):
    net = neat.nn.FeedForwardNetwork.create(genome, config)
    
    fitnesses = []

    for _ in range(runs_per_net):
        fitness = 0.0
        steps = 0
        
        fen = random_fens.get_random_fen()
        board = chess.Board(fen)
        
        while not board.is_game_over() and steps < 40:
            nn_inputs = fen_to_nn_input(board)
            output = net.activate(nn_inputs)

            from_sq, to_sq = decompress_nn_output(output[0], output[1])
            move = chess.Move(from_sq, to_sq)
            legal_moves = board.legal_moves
            if board.piece_at(from_sq):
                piece = board.piece_at(from_sq)
                fitness += 1  # Found a piece

                if move in legal_moves:
                    target = board.piece_at(to_sq)
                    if target and target.color != piece.color:
                        fitness += 6  # Captured opponent piece
                    else:
                        fitness += 3  # Legal non-capturing move

                    board.push(move)
                else:
                    legal = list(legal_moves)
                    if legal:
                        board.push(random.choice(legal))
                    fitness -= 1  # Illegal move
            else:
                legal = list(legal_moves)
                if legal:
                    board.push(random.choice(legal))
                fitness -= 0.5  # Mild penalty for invalid move
               
            steps += 1

        fitnesses.append(fitness)

    return sum(fitnesses) / len(fitnesses)


def eval_genomes(genomes, config):
    for genome_id, genome in genomes:
        genome.fitness = eval_genome(genome, config)


def run():
    # Load the config file, which is assumed to live in
    # the same directory as this script.
    local_dir = os.path.dirname(__file__)
    config_path = os.path.join(local_dir, 'config-feedforward')
    config = neat.Config(neat.DefaultGenome, neat.DefaultReproduction,
                         neat.DefaultSpeciesSet, neat.DefaultStagnation,
                         config_path)

    pop = neat.Population(config)
    stats = neat.StatisticsReporter()
    pop.add_reporter(stats)
    pop.add_reporter(neat.StdOutReporter(True))

    pe = neat.ParallelEvaluator(multiprocessing.cpu_count(), eval_genome)
    winner = pop.run(pe.evaluate)

    # Save the winner.
    with open('winner-feedforward', 'wb') as f:
        pickle.dump(winner, f)

    print(winner)

    visualize.plot_stats(stats, ylog=True, view=True, filename="feedforward-fitness.svg")
    visualize.plot_species(stats, view=True, filename="feedforward-speciation.svg")

    node_names = {-1: 'x', -2: 'dx', -3: 'theta', -4: 'dtheta', 0: 'control'}
    visualize.draw_net(config, winner, True, node_names=node_names)

    visualize.draw_net(config, winner, view=True, node_names=node_names,
                       filename="winner-feedforward.gv")
    visualize.draw_net(config, winner, view=True, node_names=node_names,
                       filename="winner-feedforward-enabled-pruned.gv", prune_unused=True)


if __name__ == '__main__':
    run()
