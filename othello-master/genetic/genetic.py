from random import random, sample, seed
from typing import List, Tuple
from tqdm import tqdm
import numpy as np
import multiprocessing as mp
from game.game import main
from ai.minimax import AI
from ai_vs_ai import compare_ai

GENERATION_COUNT = 9
POPULATION = 6
MAX_WEIGHT = 1000
CROSSOVER_PROBABILITY = 0.8
MUTATION_PROBABILITY = 0.1
SURVIVORS = int(POPULATION / 3)
BOOST_PROBABILITY = 0.3


class Gen:
    def __init__(self, features: List[float], score: int = 0):
        self.ai = AI(features)
        self.score = score


def genetic() -> AI:
    population = create_starting_population()
    for i in tqdm(range(GENERATION_COUNT), desc='Overall Progress'):
        print(f'the heurisitc weights for generation #{i} are:')
        for gen in population:
            print('\t', [f'{weight:.2f}' for weight in gen.ai.heuristic_weights])
        run_tournament(population)
        # print_population(i, population)
        population = sorted(population, key=lambda gen: gen.score, reverse=True)
        parents = choose_parents(population)
        new_babies = crossover(parents)
        population = choose_next_population(population, new_babies)
    print('the heurisitc weights for generation 9 are:')
    for gen in population:
        print('\t', [f'{weight:.2f}' for weight in gen.ai.heuristic_weights])
    run_tournament(population)
    return max(population, key=lambda gen: gen.score).ai


def print_population(i: int, population: List[Gen]):
    print(f'population #{i} is:')
    for gen in population:
        print(f'\t weights:{gen.ai.heuristic_weights}, score:{gen.score}/{POPULATION - 1}')


def choose_next_population(last_population: List[Gen], new_babies: List[Gen]) -> List[Gen]:
    fit_parents = last_population[:SURVIVORS]
    random_children = sample(new_babies, POPULATION - SURVIVORS)
    fit_parents.extend(random_children)
    return fit_parents


def boost(s0, w0, s1, w1, init_val):
    if (s0 > s1 and w0 > w1) or (s0 < s1 and w0 < w1):
        if w0 > MAX_WEIGHT / 2 and w1 > MAX_WEIGHT / 2:
            return random() * min(0.2 * MAX_WEIGHT, init_val - max(w0, w1))
        elif w0 < MAX_WEIGHT / 2 and w1 < MAX_WEIGHT / 2:
            return -random() * min(0.2 * MAX_WEIGHT, min(w0, w1))
    return 0


def crossover(parents: List[Tuple[Gen, Gen]]) -> List[Gen]:
    new_babies = []
    for couple in parents:
        if couple[0] == couple[1] or random() > CROSSOVER_PROBABILITY:
            continue
        child_features = []
        n_features = len(couple[0].ai.heuristic_weights)
        alpha = 0.5 if couple[0].score + couple[1].score == 0 else couple[0].score / (
                couple[0].score + couple[1].score)
        for i in range(n_features):
            w0 = couple[0].ai.heuristic_weights[i]
            # s0 = couple[0].score
            w1 = couple[1].ai.heuristic_weights[i]
            # s1 = couple[1].score
            child_features.append(w0 * alpha + w1 * (1.0 - alpha))
            # if random() < BOOST_PROBABILITY:
            #     child_features[i] += boost(s0, w0, s1, w1, child_features[i])
        if random() < MUTATION_PROBABILITY:
            feature_idx = int(random() * n_features)
            child_features[feature_idx] = (random() * MAX_WEIGHT + child_features[feature_idx]) / 2
        new_babies.append(Gen(child_features))
    return new_babies


def choose_parents(population):
    return [(father, mother) for father in population for mother in population]


_population = List[Gen]


def run_tournament(population: List[Gen]):
    print('\n')
    global _population
    for gen in population:
        gen.score = 0
    _population = population
    pool = mp.Pool(mp.cpu_count())
    result = pool.starmap_async(match,
                                [(i, j) for i in range(POPULATION) for j in
                                 range(i + 1, POPULATION)]).get()
    pool.close()
    pool.join()
    for winner in result:
        if winner != -1:
            population[winner].score += 1


def get_desc(l1, l2):
    return '[' + ', '.join([f'{v:.2}' for v in l1]) + '] vs [' + ', '.join([f'{v:.2}' for v in l1]) + ']'


def match(i: int, j: int):
    global _population
    winner = compare_ai(_population[i].ai, _population[j].ai)
    return i if winner == "bob" else j if winner == "alice" else -1


def create_starting_population() -> List[Gen]:
    population = []
    for i in range(POPULATION):
        # population.append(Gen([random() * MAX_WEIGHT for j in range(6)]))
        nparr = np.random.uniform(low=0, high=MAX_WEIGHT, size=(POPULATION,))
        population.append(Gen(nparr.tolist()))
    return population


if __name__ == '__main__':
    ai = genetic()
    with open('../optimized_heuristic_weights.txt', 'a') as output_file:
        output_file.write('\n' + ', '.join(str(weight) for weight in ai.heuristic_weights))
    # main()
