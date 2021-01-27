from time import time
from typing import List, Dict

DEFAULT_HEURISTIC_WEIGHTS = [10, 801.724, 382.026, 74.396, 10, 78.922]


def diff_ratio(mp: Dict) -> float:
    if mp['b'] + mp['w'] == 0:
        return 0
    return (mp['b'] - mp['w']) / (mp['b'] + mp['w'])


class OthelloHeuristic:
    def __init__(self, metrics, possible_actions, weights: List[float] = None):
        if weights is None:
            weights = DEFAULT_HEURISTIC_WEIGHTS
        self.metrics = metrics
        self.weights = weights
        self.possible_actions = possible_actions

    def f(self, grid):
        self.metrics.n_heuristic += 1
        start_time = time()
        weighted_tiles_count_difference_measure = 0

        plus_neg_map = {'w': -1, 'b': 1}
        tot_tiles = {'w': 0, 'b': 0}
        front_tiles = {'w': 0, 'b': 0}

        dx_neighbor = [-1, -1, 0, 1, 1, 1, 0, -1]
        dy_neighbor = [0, 1, 1, 1, 0, -1, -1, -1]

        cell_weights = [[20, -3, 11, 8, 8, 11, -3, 20],
                        [-3, -7, -4, 1, 1, -4, -7, -3],
                        [11, -4, 2, 2, 2, 2, -4, 11],
                        [8, 1, 2, -3, -3, 2, 1, 8],
                        [8, 1, 2, -3, -3, 2, 1, 8],
                        [11, -4, 2, 2, 2, 2, -4, 11],
                        [-3, -7, -4, 1, 1, -4, -7, -3],
                        [20, -3, 11, 8, 8, 11, -3, 20]]

        # Piece difference, disks and disk squares
        for i in range(8):
            for j in range(8):
                if grid[i][j] is not None:
                    weighted_tiles_count_difference_measure += plus_neg_map[grid[i][j]] * cell_weights[i][j]
                    tot_tiles[grid[i][j]] += 1
                    for k in range(8):
                        x = i + dx_neighbor[k]
                        y = j + dy_neighbor[k]
                        if 0 <= x < 8 and 0 <= y < 8 and grid[x][y] is None:
                            front_tiles[grid[i][j]] += 1

        tiles_count_measure = 100.00 * diff_ratio(tot_tiles)
        front_tiles_measure = -100.00 * diff_ratio(front_tiles)

        # Corners
        corner_tiles = {'b': 0, 'w': 0}
        corner_neighbors = {'b': 0, 'w': 0}
        for i in [0, 7]:
            for j in [0, 7]:
                if grid[i][j] is not None:
                    corner_tiles[grid[i][j]] += 1
                else:
                    for k in range(8):
                        x = i + dx_neighbor[k]
                        y = j + dy_neighbor[k]
                        if 0 <= x < 8 and 0 <= y < 8 and grid[x][y] is not None:
                            corner_neighbors[grid[x][y]] += 1

        corner_tiles_measure = 25 * diff_ratio(corner_tiles)
        corner_neighbors_measure = -(100 / 12) * diff_ratio(corner_neighbors)

        # Mobility
        my_player_number = 1
        opp_player_number = -1
        actions_count = {'b': self.possible_actions(grid, my_player_number, True),
                         'w': self.possible_actions(grid, opp_player_number, True)}
        actions_count_measure = 100 * diff_ratio(actions_count)

        score = (self.weights[0] * tiles_count_measure) + (self.weights[1] * corner_tiles_measure) + (
                self.weights[2] * corner_neighbors_measure) + (self.weights[3] * front_tiles_measure) + (
                        self.weights[4] * weighted_tiles_count_difference_measure) + (
                        self.weights[5] * actions_count_measure)
        self.metrics.heuristic_time += time() - start_time
        return score

# 0, 10, 10, 6, 12, 6