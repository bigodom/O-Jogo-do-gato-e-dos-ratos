import platform
from os import system


def print_table(table: list[list[int]]) -> None:
    row_count = 0
    print("-----------------------------------------\n")
    print("     0    1    2    3    4    5    6    7")
    for row in table:
        for indx, cell in enumerate(row):
            if cell == 0:
                if indx == 0:
                    print(f"{row_count}  |", " ", "|", end="")
                    row_count += 1
                else:
                    print("|", " ", "|", end="")
            elif cell == 1:
                if indx == 0:
                    print(f"{row_count}  |", "R", "|", end="")
                    row_count += 1
                else:
                    print("|", "R", "|", end="")
            else:
                if indx == 0:
                    print(f"{row_count}  |", "C", "|", end="")
                    row_count += 1
                else:
                    print("|", "C", "|", end="")
        print("\n")
    print("-----------------------------------------")


def get_user_input() -> list[int, int]:
    while True:
        try:
            x, y = input("Digite as coordenadas (x,y) no tabuleiro: \n").split()
            x = int(x)
            y = int(y)
            return [x, y]
        except ValueError:
            print(
                "\nErro! Digite valores números no formato: X Y. Verifique se os valores são númericos e estão separados por um espaço.\n"
            )


def clear_console():
    os = platform.system().lower()
    if "windows" in os:
        system("cls")
    else:
        system("clear")


def get_empty_cells(table: list[list[int]]) -> list[list[int, int]]:
    cells = []
    for x, row in enumerate(table):
        for y, cell in enumerate(row):
            if cell == 0:
                cells.append([x, y])

    return cells


def get_diagonal_cells_by_position(x: int, y: int) -> list:
    cells = []
    n = 8
    for i in range(n):
        if x + i < n and y + i < n:
            cells.append([x + i, y + i])
        if x - i >= 0 and y - i >= 0:
            cells.append([x - i, y - i])

    for i in range(n):
        if x + i < n and y - i >= 0:
            cells.append([x + i, y - i])
        if x - i >= 0 and y + i < n:
            cells.append([x - i, y + i])

    print(f"DIAGONAIS: {cells}")

    return cells


def get_cat_x_path(table: list[list[int]], position: list[int, int]) -> set[tuple[int, int]]:
    cat_x, cat_y = position
    cells = set()

    # A partir da posição atual do gato (X) para frente
    for index, value in enumerate(table[cat_x][cat_y:]):
        if value == 0:
            cells.add((cat_x, index+cat_y))

        if value == 1:
            cells.add((cat_x, index+cat_y))
            break

    # A partir da posição atual do gato (X) para tras
    for index, value in enumerate(table[cat_x][cat_y::-1]):
        y_axis = cat_y - index

        if value == 0:
            cells.add((cat_x, y_axis))

        if value == 1:
            cells.add((cat_x, y_axis))
            break

    return cells


def get_cat_y_path(table: list[list[int]], position: list[int, int]) -> set[tuple[int, int]]:
    cat_x, cat_y = position
    cells = set()

    # Percorrendo para cima da posição Y
    for i in range(cat_x, -1, -1):
        value = table[i][cat_y]

        if value == 0:
            cells.add((i, cat_y))

        if value == 1:
            cells.add((i, cat_y))
            break

    # Percorrendo para baixo da posição Y
    for i in range(cat_x+1, len(table)):
        value = table[i][cat_y]

        if value == 0:
            cells.add((i, cat_y))

        if value == 1:
            cells.add((i, cat_y))
            break

    return cells
