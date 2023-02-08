import platform
from os import system


def print_table(table: list[list[int]]) -> None:
    print("-----------------------------------------")
    for row in table:
        for cell in row:
            if cell == 0:
                print("|", " ", "|", end="")
            elif cell == 1:
                print("|", "R", "|", end="")
            else:
                print("|", "C", "|", end="")
        print("\n")
    print("-----------------------------------------")


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

    return cells
