from random import random


def starting_array():
    array = [[None for i in range(8)] for j in range(8)]
    array[3][3] = "w"
    array[4][4] = "w"
    array[3][4] = "b"
    array[4][3] = "b"
    return array


def extract_0(act) -> int:
    return act.choice[0]


def extract_1(act) -> int:
    return act.choice[1]


def extract_0_plus_1(act) -> int:
    return act.choice[0] + act.choice[1]


def extract_0_minus_1(act) -> int:
    return act.choice[0] - act.choice[1]


def extract_random(act) -> float:
    return random() * 100
