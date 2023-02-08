from math import inf

from utils import (
    clear_console,
    get_diagonal_cells_by_position,
    get_empty_cells,
    print_table,
)

HUMAN = 2
AI = 1
TABLE = [
    [0, 0, 0, 0, 0, 0, 0, 0],
    [1, 1, 1, 0, 0, 1, 1, 1],
    [0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 2, 0, 0, 0, 0],
]
CURRENT_PLAYER = 2
CURRENT_CAT_POSITION = [7, 3]

print_table(TABLE)


def make_human_move() -> None:
    current_x, current_y = CURRENT_CAT_POSITION
    while True:
        x, y = input("Digite as coordenadas (x,y) no tabuleiro: \n").split()
        x = int(x)
        y = int(y)

        if [x, y] not in get_diagonal_cells_by_position(current_x, current_y) and TABLE[
            x
        ][y] == 0:
            break
        else:
            clear_console()
            print_table(TABLE)
            print("Movimento inválido!\n")


make_human_move()
