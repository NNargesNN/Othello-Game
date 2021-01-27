from random import random


def starting_array():
    array = [[None for i in range(8)] for j in range(8)]
    array[3][3] = "w"
    array[4][4] = "w"
    array[3][4] = "b"
    array[4][3] = "b"
    return array


def rand_index(mx: int) -> int:
    return int(random() * mx)
