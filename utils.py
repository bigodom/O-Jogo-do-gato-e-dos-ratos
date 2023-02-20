"""
Módulo de utilidade, para funções auxiliares.
@author: Filipe Augusto, Pedro Augusto
"""

import platform
from os import system


def print_table(table: list[list[int]]) -> None:
    """
    Função que imprime o tabuleiro no console
    :param table: Estado atual do tabuleiro
    """
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
    """
    Função que trata a entrada de dados do jogador humano
    :return: Lista no formato [x,y] contendo a linha e a coluna no tabuleiro respectivamente
    """
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
    """
    Função que limpa o console de acordo com o S.O
    """
    os = platform.system().lower()
    if "windows" in os:
        system("cls")
    else:
        system("clear")


def get_empty_cells(table: list[list[int]]) -> list[list[int, int]]:
    """
    Função que retorna as posições vazias no tabuleiro
    :param table: Estado atual do tabuleiro
    :return: Posições vazias no tabuleiro
    """
    cells = []
    for x, row in enumerate(table):
        for y, cell in enumerate(row):
            if cell == 0:
                cells.append([x, y])

    return cells


def get_diagonal_cells_by_position(x: int, y: int) -> list:
    """
    Função que retorna as diagonais de uma determinada posição
    :param x: Linha no tabuleiro
    :param y: Coluna no tabuleiro
    :return: Células na diagonal da posição
    """
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


def get_cat_x_path(table: list[list[int]], position: list[int, int]) -> set[tuple[int, int]]:
    """
    Função que obtem o caminho no eixo X do gato
    :param table: Estado atual do tabuleiro
    :param position: Posição atual do gato
    :return: Conjunto com as posições no eixo X em que o gato pode se movimentar
    """
    cat_x, cat_y = position
    cells = set()

    # A partir da posição atual do gato (X) para frente
    for index, value in enumerate(table[cat_x][cat_y:]):
        if value == 0:
            cells.add((cat_x, index + cat_y))

        if value == 1:
            cells.add((cat_x, index + cat_y))
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
    """
    Função que obtem o caminho no eixo Y do gato
    :param table: Estado atual do tabuleiro
    :param position: Posição atual do gato
    :return: Conjunto com as posições no eixo Y em que o gato pode se movimentar
    """
    cat_x, cat_y = position
    cells = set()

    # A partir da posição atual do gato (Y) para cima
    for i in range(cat_x, -1, -1):
        value = table[i][cat_y]

        if value == 0:
            cells.add((i, cat_y))

        if value == 1:
            cells.add((i, cat_y))
            break

    # A partir da posição atual do gato (Y) para baixo
    for i in range(cat_x + 1, len(table)):
        value = table[i][cat_y]

        if value == 0:
            cells.add((i, cat_y))

        if value == 1:
            cells.add((i, cat_y))
            break

    return cells





def map_y_to_rat(y):
    if y <= 2:
        return y
    if y == 5:
        return 3
    if y == 6:
        return 4
    if y == 7:
        return 5