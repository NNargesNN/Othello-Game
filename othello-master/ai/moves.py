BOARD_SIZE = 8


def is_valid_move(array, player, x, y):
    if player == -1 or player == 0:
        color = "w"
    else:
        color = "b"

    if array[x][y] is not None:
        return False

    else:
        # dar heyne bazi baraye update e array momkene null bashe va hich harekati mojaz nist in beyn
        valid_move = False
        SurroundingCells = []

        x_min = max(0, x - 1)
        x_max = min(x + 2, 8)
        y_min = max(0, y - 1)
        y_max = min(y + 2, 8)

        for i in range(x_min, x_max):
            for j in range(y_min, y_max):
                if array[i][j] is not None:
                    valid_move = True
                    SurroundingCells.append([i, j])

        if not valid_move:
            return False
        else:
            valid = False
            for Cell in SurroundingCells:
                cell_X = Cell[0]
                cell_Y = Cell[1]
                if array[cell_X][cell_Y] == color:
                    continue
                else:
                    delta_x = cell_X - x
                    delta_y = cell_Y - y
                    temp_x = cell_X
                    temp_y = cell_Y
                    while 0 <= temp_x <= 7 and 0 <= temp_y <= 7:
                        if array[temp_x][temp_y] == None:
                            break
                        if array[temp_x][temp_y] == color:
                            valid = True
                            break
                        temp_x += delta_x
                        temp_y += delta_y
            return valid


def final_score(array):
    score = 0
    for x in range(8):
        for y in range(8):
            if array[x][y] == "b":
                score += 1
            elif array[x][y] == "w":
                score -= 1

    return 100 * score / (BOARD_SIZE * BOARD_SIZE)
