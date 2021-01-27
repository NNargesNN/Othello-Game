from copy import deepcopy
from faker import Faker
from random import random
from time import time
from typing import List

from ai.action import Action, Scorer
from ai.moves import is_valid_move
from heuristic.heuristic import OthelloHeuristic, DEFAULT_HEURISTIC_WEIGHTS
from utils.utils import *

faker = Faker()
PLAYER_COLORS = ['w', 'b']
MINIMAX_DEPTH = 8
BRANCHING_FACTOR = 7
inf = float("inf")
with open('../optimized_scorer_weights.txt', 'r') as optimized_weights_file:
    OPTIMIZED_SCORER_WEIGHTS = [float(weight) for weight in optimized_weights_file.readline().split(',')]


class Metrics:
    n_heuristic = 0
    heuristic_time = 0
    nodes = 0
    prune_time = 0

    @staticmethod
    def reset():
        Metrics.n_heuristic = 0
        Metrics.heuristic_time = 0
        Metrics.prune_time = 0
        Metrics.nodes = 0

    @staticmethod
    def print_metrics():
        print(f'\nn_heuristic = {Metrics.n_heuristic}')
        print(f'heuristic_time = {Metrics.heuristic_time}')
        print(f'average heuristic time: {Metrics.heuristic_time / Metrics.n_heuristic}')
        print(f'prune_time = {Metrics.prune_time}')
        print(f'nodes = {Metrics.nodes}')


def move(old_array, player, x, y):
    new_array = deepcopy(old_array)
    if player == -1:
        color = "w"
    else:
        color = "b"
    new_array[x][y] = color

    neighbours = []
    for i in range(max(0, x - 1), min(x + 2, 8)):
        for j in range(max(0, y - 1), min(y + 2, 8)):
            if new_array[i][j] is not None:
                neighbours.append([i, j])

    convert = []

    for neighbour in neighbours:
        neighX = neighbour[0]
        neighY = neighbour[1]
        # Check if the neighbour is of a different colour - it must be to form a line
        if new_array[neighX][neighY] == color:
            continue
        # The path of each individual line
        path = []

        # Determining direction to move
        deltaX = neighX - x
        deltaY = neighY - y

        tempX = neighX
        tempY = neighY

        # While we are in the bounds of the board
        while 0 <= tempX <= 7 and 0 <= tempY <= 7:
            path.append([tempX, tempY])
            value = new_array[tempX][tempY]
            # If we reach a blank tile, we're done and there's no line
            if value is None:
                break
            # If we reach a tile of the player's colour, a line is formed
            if value == color:
                # Append all of our path nodes to the convert array
                for node in path:
                    convert.append(node)
                break
            # Move the tile
            tempX += deltaX
            tempY += deltaY

    # Convert all the appropriate tiles
    for node in convert:
        new_array[node[0]][node[1]] = color

    return new_array

    '''
     * Assuming my_color stores your color and opp_color stores opponent's color
     * '-' indicates an empty square on the board
     * 'b' indicates a black tile and 'w' indicates a white tile on the board
     '''


def possible_actions(array, player, count_only=False):
    boards = []
    choices = []

    for x in range(8):
        for y in range(8):
            if is_valid_move(array, player, x, y):
                boards.append(move(array, player, x, y))
                choices.append([x, y])
    if count_only:
        return len(boards)
    return boards, choices


DEFAULT_OTHELLO_HEURISTIC = OthelloHeuristic(Metrics, possible_actions, DEFAULT_HEURISTIC_WEIGHTS)


class AI:
    def __init__(self, heuristic_weights: List[float] = None):
        self.name = faker.name()
        if heuristic_weights is None:
            self.heuristic_weights = OPTIMIZED_SCORER_WEIGHTS
        else:
            self.heuristic_weights = heuristic_weights
        if heuristic_weights is not None:
            self.heuristic = OthelloHeuristic(Metrics, possible_actions, heuristic_weights)
        else:
            self.heuristic = DEFAULT_OTHELLO_HEURISTIC
        self.scorer_weights = OPTIMIZED_SCORER_WEIGHTS
        self.scorers = [
            Scorer(extract_0, 0, 7, self.scorer_weights[0]),
            Scorer(extract_1, 0, 7, self.scorer_weights[1]),
            Scorer(extract_0_plus_1, 0, 14, self.scorer_weights[2]),
            Scorer(extract_0_minus_1, 0, 7, self.scorer_weights[3]),
            Scorer(extract_random, 0, 100, self.scorer_weights[4]),
        ]

    def minimax(self, array, player) -> Action:
        # Metrics.reset()
        minimax_player = -1 if player == 0 else 1
        result = self.minimax_(array, minimax_player, MINIMAX_DEPTH, -inf, inf)
        # Metrics.print_metrics()
        # print(f'{nodes} total nodes visited')
        return result


    def pruned_actions(self, array, player):
        all_boards, all_choices = possible_actions(array, player)
        all_actions = [
            Action(all_boards[i], all_choices[i], 0)
            for i in range(len(all_boards))
        ]
        for scorer in self.scorers:
            scorer.score(all_actions)
        sorted_actions = sorted(all_actions, key=Action.get_score, reverse=True)
        return sorted_actions[:BRANCHING_FACTOR]

    def minimax_(self, array, player, depth, alpha, beta, can_pass=True):
        start_time = time()
        actions = self.pruned_actions(array, player)
        Metrics.prune_time += time() - start_time
        Metrics.nodes += 1

        if len(actions) == 0:
            if can_pass:
                return self.minimax_(array, -player, depth - 1, alpha, beta, False)
            else:
                return Action(array, None, self.heuristic.f(array))

        if depth == 0:
            return Action(array, None, self.heuristic.f(array))

        v = -inf * player
        best_action = Action(None, None, v)
        for i, action in enumerate(actions):
            current_action = self.minimax_(action.board, -player, depth - 1, alpha, beta)
            if (current_action.minimax - v) * player > 0:
                v = current_action.minimax
                best_action.board = action.board
                best_action.choice = action.choice
                best_action.minimax = v
            if not (alpha < v < beta):
                break
            if player == 1:
                alpha = max(alpha, v)
            else:
                beta = min(beta, v)
        return best_action
