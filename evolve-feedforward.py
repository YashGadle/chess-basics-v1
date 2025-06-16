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
        fen = random_fens.get_random_fen()
        board = chess.Board(fen)
        
        fitness = 0.0
        steps = 0
        
        while not board.is_game_over() and steps < 10:
            nn_inputs = fen_to_nn_input(board)
            output = net.activate(nn_inputs)

            from_sq, to_sq = decompress_nn_output(output[0], output[1])
            move = chess.Move(from_sq, to_sq)

            if(board.piece_at(from_sq)):
                fitness += 1  # Reward for finding a piece
                if move in board.legal_moves:
                    board.push(move)
                    print(board, move, move in board.legal_moves)
                    print("\n")
                    fitness += 5  # Reward legal move
                else:
                    fitness -= 1
            else:
                fitness -= 0.5
               

            steps += 1

        fitnesses.append(fitness)

    # The genome's fitness is its worst performance across all runs.
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
