from ai.minimax import AI, possible_actions
from utils.utils import starting_array


def print_board(move, array):
    print(f'board #{move} is:')
    for i in range(8):
        for j in range(8):
            print(array[i][j] if array[i][j] is not None else '-', end=', ' if j + 1 < 8 else '\n')


def compare_ai(bob: AI, alice: AI) -> str:
    array = starting_array()
    player = 1
    # print('*' * 20)
    moves_cnt = 0
    while possible_actions(array, 1, True) > 0 or possible_actions(array, -1, True) > 0:
        if player == 1:
            array = bob.minimax(array, player).board
        else:
            array = alice.minimax(array, player).board
        player = 1 - player
        moves_cnt += 1
        # print_board(moves_cnt, array)
    tiles = [0, 0]
    for i in range(8):
        for j in range(8):
            if array[i][j] == "w":
                tiles[0] += 1
            elif array[i][j] == "b":
                tiles[1] += 1
    if tiles[0] == tiles[1]:
        print(f'{bob.name} drew against {alice.name}')
        return "draw"
    elif tiles[0] > tiles[1]:
        print(f'{bob.name} won against {alice.name}')
        return "bob"
    else:
        print(f'{bob.name} lost to {alice.name}')
        return "alice"
