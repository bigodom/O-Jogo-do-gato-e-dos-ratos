import platform
from math import inf
from os import system

"""
Módulo de utilidade, para funções auxiliares.
@author: Filipe Augusto, Pedro Augusto
"""


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
            print("\nErro! Digite valores números no formato: X Y. Verifique se os valores são númericos e estão "
                  "separados por um espaço.\n")


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
    """
    Retorna o rato baseado na coluna em questão
    :param y: Coluna no tabuleiro
    :return: Rato baseado na coluna
    """
    if y <= 2:
        return y
    if y == 5:
        return 3
    if y == 6:
        return 4
    if y == 7:
        return 5


def get_alive_rats_from_state(state: list[list[int]]) -> int:
    """
    Obtem a quantidade de ratos vivos no estado atual
    :param state: Estado atual
    :return: Quantide de ratos vivos
    """
    alive_rats = 0
    for x, row in enumerate(state):
        for y, cell in enumerate(row):
            if cell == 1:
                alive_rats += 1

    return alive_rats


def get_cat_position_from_state(state: list[list[int]]) -> list[int, int]:
    """
    Obtem a posição do gato no estado atual
    :param state: Estado atual
    :return: Posição do gato no estado atual
    """
    position = None
    for x, row in enumerate(state):
        for y, cell in enumerate(row):
            if cell == 2:
                position = [x, y]

    return position


def get_rats_positions_from_state(state: list[list[int]]):
    """
    Obtém posições dos ratos no estado atual
    :param state: Estado atual
    :return: Posições dos ratos no estado atual
    """
    positions = {0: None, 1: None, 2: None, 3: None, 4: None, 5: None}

    for x, row in enumerate(state):
        for y, cell in enumerate(row):
            if cell == 1:
                positions[map_y_to_rat(y)] = [x, y]

    return positions


def get_rats_possible_moves_from_state(state: list[list[int]]):
    """
    Obtem os possíveis movimentos de cada rato no estado atual
    :param state: Estado atual
    :return: Possíveis movimentos para cada rato
    """
    moves = []
    positions = get_rats_positions_from_state(state)
    cat_x, cat_y = get_cat_position_from_state(state)

    for rat, position in positions.items():
        if position is not None:
            x, y = position
            if x != inf or y != inf or x != 7:
                if state[x + 1][y] == 0:
                    moves.append([rat, x + 1, y])
                if y != 7 and state[x + 1][y + 1] == 2:
                    moves.append([rat, x + 1, y + 1])
                if y != 0 and state[x + 1][y - 1] == 2:
                    moves.append([rat, x + 1, y - 1])
                if x == 1:
                    moves.append([rat, x + 2, y])

    return moves


def get_possible_moves_from_rat(state: list[list[int]], x: int, y: int):
    """
    Obtem os possíveis movimentos de determinado rato no estado atual
    :param state: Estado atual
    :param x: Linha em que o rato está
    :param y: Coluna em que o rato está
    :return: Possíveis movimentos do rato
    """
    rat_moves = []
    if x != inf or y != inf or x != 7:
        if state[x + 1][y] == 0:
            rat_moves.append([x, y + 1])
        if y != 7 and state[x + 1][y + 1] == 2:
            rat_moves.append([x + 1, y + 1])
        if y != 0 and state[x + 1][y - 1] == 2:
            rat_moves.append([x + 1, y - 1])
        if x == 1:
            rat_moves.append([x + 2, y])

    return rat_moves


def distance_between(rat: list[int, int], cat: list[int, int]):
    """
    Obtem a distancia entre o rato e o gato no eixo X
    :param rat: Posição do rato
    :param cat: Posição do gato
    :return: Distancia entre o gato e rato
    """
    rat_x, rat_y = rat
    cat_x, cat_y = cat
    if rat_x > cat_x:
        distance = rat_x - cat_x
    else:
        distance = cat_x - rat_x

    return distance


def get_distance_from_entities(rat: list[int, int], cat: list[int, int]):
    """
    Obtem distancia real entre o rato e o gato
    :param rat: Posição do rato
    :param cat: Posição do gato
    :return: Distancia numérica nos eixos X e Y entre o gato e rato
    """
    rat_x, rat_y = rat
    cat_x, cat_y = cat

    if rat_y == cat_y:
        distance = distance_between(rat, cat)
    elif rat_y > cat_y:
        distance = (rat_y - cat_y) + distance_between(rat, cat)
    else:
        distance = (cat_y - rat_y) + distance_between(rat, cat)

    return distance


def max_heuristic(state: list[list[int]]):
    """
    Heurística para o jogador MAX, baseada na distância entre os ratos e o gato
    :param state: Estado atual do jogo
    :return: Valor numérico de melhor distância dos ratos para o gato
    """
    rats = get_rats_positions_from_state(state)
    cat_x, cat_y = get_cat_position_from_state(state)
    max_distance_from_cat = -inf

    for rat, position in rats.items():
        if position is not None:
            rat_x, rat_y = position
            current_distance = get_distance_from_entities([rat_x, rat_y], [cat_x, cat_y]) - 1
            if current_distance > max_distance_from_cat:
                max_distance_from_cat = current_distance

    return max_distance_from_cat


def min_heuristic(state: list[list[int]]):
    """
    Heurística para o jogador MIN, baseadda na distância entre os ratos e o gato
    :param state: Estado atual do jogo
    :return: Valor numérico de melhor distância entre o gato e os ratos
    """
    rats = get_rats_positions_from_state(state)
    cat_x, cat_y = get_cat_position_from_state(state)
    closest_rat = +inf

    for rat, position in rats.items():
        if position is not None:
            rat_x, rat_y = position
            current_distance = get_distance_from_entities([rat_x, rat_y], [cat_x, cat_y]) - 1
            if current_distance < closest_rat:
                closest_rat = current_distance

    return closest_rat


def is_end_state(state: list[list[int]]):
    """
    Avalia se é um estado final
    :param state: Estado atual
    :return: Avaliação se é um estado final e quem é o vencedor
    """
    for cell in state[7]:
        if cell == 1:
            return [True, 1]

    if get_alive_rats_from_state(state) == 0:
        return [True, -1]

    cat = get_cat_position_from_state(state)
    if not cat:
        return [True, 1]

    return [False, 0]
