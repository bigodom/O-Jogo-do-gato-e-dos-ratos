from utils import clear_console, get_user_input, print_table, get_cat_x_path, get_cat_y_path, map_y_to_rat
from math import inf
from copy import deepcopy
from random import choice

"""
@author: Filipe Augusto, Pedro Augusto
"""

"""
Módulo core para executar o Jogo do gato e dos ratos.
"""


class Game:
    def __init__(self) -> None:
        self.TABLE = [
            [0, 0, 0, 0, 0, 0, 0, 0],
            [1, 1, 1, 0, 0, 1, 1, 1],
            [0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 2, 0, 0, 0, 0],
        ]
        self.HUMAN = 2
        self.AI = 1
        self.CURRENT_PLAYER = 1
        self.CURRENT_CAT_POSITION = [7, 3]
        self.MIN_CAT_POSITION = [7, 3]
        self.ALIVE_RATS = 6
        self.MAX_ALIVE_RATS = 6
        self.CURRENT_RATS_POSITION = {
            0: [1, 0],
            1: [1, 1],
            2: [1, 2],
            3: [1, 5],
            4: [1, 6],
            5: [1, 7],
        }
        self.MAX_RATS_POSITION = {
            0: [1, 0],
            1: [1, 1],
            2: [1, 2],
            3: [1, 5],
            4: [1, 6],
            5: [1, 7],
        }
        self.CURRENT_RATS_MOVES_COUNT = {
            0: 0,
            1: 0,
            2: 0,
            3: 0,
            4: 0,
            5: 0,
        }
        self.MAX_RATS_MOVES_COUNT = {
            0: 0,
            1: 0,
            2: 0,
            3: 0,
            4: 0,
            5: 0,
        }
        self.WINNER = None
        self.FIRST_TURN = True

    def __make_human_move(self) -> None:
        """
        Função que executa o movimento do gato
        :return: Tabuleiro atualizado com nova posição do gato
        """
        possible_cat_moves = self.__get_cat_possible_moves()

        while True:
            print(f"Possíveis movimentos: \n{possible_cat_moves}\n")
            x, y = get_user_input()

            if (x, y) in possible_cat_moves:
                self.__exec_move(x, y)
                break
            else:
                clear_console()
                print_table(self.TABLE)
                print("Movimento inválido!\n")

    def __get_rats_possible_moves(self, is_max: bool = False, copy: list[list[int]] | None = None) -> dict:
        """
        Função que retorna os possíveis movimentos para cada rato vivo
        :return: Dicionário com movimentos possíveis para cada rato
        """
        cells = {0: [], 1: [], 2: [], 3: [], 4: [], 5: []}

        if is_max:
            positions = self.MAX_RATS_POSITION
            moves_count = self.MAX_RATS_MOVES_COUNT
            table = copy
        else:
            positions = self.CURRENT_RATS_POSITION
            moves_count = self.CURRENT_RATS_MOVES_COUNT
            table = self.TABLE

        for rat, position in positions.items():
            rat_x, rat_y = position
            current_rat_moves = []

            if rat_x == inf or rat_x == 7:
                continue

            else:
                if table[rat_x + 1][rat_y] == 0:
                    current_rat_moves.append([rat_x + 1, rat_y])

                if rat_y != 7:
                    if table[rat_x + 1][rat_y + 1] == 2:
                        current_rat_moves.append([rat_x + 1, rat_y + 1])
                if rat_y != 0:
                    if table[rat_x + 1][rat_y - 1] == 2:
                        current_rat_moves.append([rat_x + 1, rat_y + 1])

            if moves_count[rat] == 0 and rat_x != inf:
                current_rat_moves.append([rat_x + 2, rat_y])
                cells[rat] = current_rat_moves
            else:
                cells[rat] = current_rat_moves

        return cells

    def __get_cat_possible_moves(self, copy: list[list[int]] | None = None):
        """
        Função que retorna uma lista de movimentos possíveis para o jogador humano
        :return: Lista de movimentos possíveis para o gato
        """
        if not copy:
            x_axis_moves = get_cat_x_path(self.TABLE, self.CURRENT_CAT_POSITION)
            y_axis_moves = get_cat_y_path(self.TABLE, self.CURRENT_CAT_POSITION)
            moves = x_axis_moves | y_axis_moves
        else:
            x_axis_moves = get_cat_x_path(copy, self.MIN_CAT_POSITION)
            y_axis_moves = get_cat_y_path(copy, self.MIN_CAT_POSITION)
            moves = x_axis_moves | y_axis_moves

        return sorted(moves, key=lambda pair: (pair[0], pair[1]))

    def __exec_move(self, x: int, y: int, rat: int | None = None) -> None:
        """
        Executa o movimento escolhido pelo jogador atual
        :param x: Linha no tabuleiro
        :param y: Coluna no tabuleiro
        :param rat: Rato escolhido, caso seja a vez da IA
        :return: Tabuleiro atualizado com novas posições
        """
        if self.CURRENT_PLAYER == 2:
            previous_cat_x, previous_cat_y = self.CURRENT_CAT_POSITION
            if self.TABLE[x][y] == 1:
                self.ALIVE_RATS -= 1
                self.CURRENT_RATS_POSITION[map_y_to_rat(y)] = [inf, inf]
                self.MAX_RATS_POSITION[map_y_to_rat(y)] = [inf, inf]
            self.TABLE[previous_cat_x][previous_cat_y] = 0
            self.TABLE[x][y] = self.CURRENT_PLAYER
            self.CURRENT_CAT_POSITION = [x, y]
            self.MIN_CAT_POSITION = [x, y]
            self.CURRENT_PLAYER = 1
            clear_console()
            print_table(self.TABLE)
        else:
            previous_rat_x, previous_rat_y = self.CURRENT_RATS_POSITION[rat]
            self.TABLE[x][y] = self.CURRENT_PLAYER
            self.TABLE[previous_rat_x][previous_rat_y] = 0
            self.CURRENT_RATS_POSITION[rat] = [x, y]
            self.MAX_RATS_POSITION[rat] = [x, y]
            self.MAX_RATS_MOVES_COUNT[rat] += 1
            self.CURRENT_RATS_MOVES_COUNT[rat] += 1
            self.CURRENT_PLAYER = 2
            clear_console()
            print_table(self.TABLE)

    def __eval(self, copy: list[list[int] | None]):
        for cell in copy[7]:
            if cell == 1:
                return 1

        if self.MAX_ALIVE_RATS == 0:
            return -1

        cat_x, cat_y = self.MIN_CAT_POSITION
        for _, position in self.MAX_RATS_POSITION.items():
            rat_x, rat_y = position
            if rat_x == cat_x - 1 and (rat_y == cat_y + 1 and rat_y == cat_y - 1):
                return 1

        return 0

    def __exec_max_move(self, copy: list[list[int]], x: int, y: int, rat: int):
        previous_x, previous_y = self.MAX_RATS_POSITION[rat]
        if previous_x != inf:
            copy[previous_x][previous_y] = 0
            copy[x][y] = 1
            self.MAX_RATS_POSITION[rat] = [x, y]
            self.MAX_RATS_MOVES_COUNT[rat] += 1

    def __exec_min_move(self, copy: list[list[int]], x: int, y: int):
        previous_x, previous_y = self.MIN_CAT_POSITION
        if copy[x][y] == 1:
            self.MAX_ALIVE_RATS -= 1
            self.MAX_RATS_POSITION[map_y_to_rat(y)] = [inf, inf]
        copy[previous_x][previous_y] = 0
        copy[x][y] = 2
        self.MIN_CAT_POSITION = [x, y]

    def __get_rats_max_possible_moves(self, state: list[list[int]]):
        moves = []
        for rat, position in self.MAX_RATS_POSITION.items():
            for cell in self.__get_rats_possible_moves(is_max=True, copy=state)[rat]:
                x, y = cell
                if x != inf and y != inf:
                    moves.append([rat, x, y])

        return moves

    def __minimax(self, state: list[list[int]], depth: int, alpha: int, beta: int, max_player: bool):

        if self.__eval(state) != 0 or depth == 0:
            utility = self.__eval(state)
            return utility

        if max_player:
            max_eval = -inf
            for action in self.__get_rats_max_possible_moves(state):
                new_state = deepcopy(state)
                rat, x, y = action
                self.__exec_max_move(new_state, x, y, rat)
                current_eval = self.__minimax(new_state, depth - 1, alpha, beta, False)
                if current_eval > max_eval:
                    max_eval = current_eval
                alpha = max(alpha, current_eval)
                if beta <= alpha:
                    break
            return max_eval

        else:
            min_eval = inf
            for move in self.__get_cat_possible_moves(state):
                new_state = deepcopy(state)
                x, y = move
                self.__exec_min_move(new_state, x, y)
                current_eval = self.__minimax(new_state, depth - 1, alpha, beta, True)
                if current_eval < min_eval:
                    min_eval = current_eval
                beta = min(beta, current_eval)
                if beta <= alpha:
                    break
            return min_eval

    def __check_win(self) -> list[bool, int] | bool:
        """
        Função que verifica se algum jogador venceu o jogo
        :return: Jogador vencedor ou False se o jogo não possui vencedor
        """

        for cell in self.TABLE[7]:
            if cell == 1:
                self.WINNER = 1
                return [True, 1]

        if self.ALIVE_RATS == 0:
            self.WINNER = 2
            return [True, 2]

        cat_x, cat_y = self.CURRENT_CAT_POSITION
        for _, position in self.CURRENT_RATS_POSITION.items():
            rat_x, rat_y = position
            if rat_x == cat_x - 1 and (rat_y == cat_y + 1 and rat_y == cat_y - 1):
                self.WINNER = 1
                return [True, 1]

        return False

    def __make_ia_move(self) -> None:
        """
        Função que executa o algoritmo MINMAX e realiza o movimento da IA
        Caso seja o primeiro turno, é executado um movimento aleatório
        Caso contrario, é executado o minimax para obter o valor da melhor jogada
        Após obter o valor, percorremos o array de movimentos para encontrar o movimento com respectivo valor
        :return: Tabuleiro atualizado com novas posições
        """
        print("IA pensando ...")

        if self.FIRST_TURN:
            moves = self.__get_rats_possible_moves()
            x, y = choice(choice(moves))
            best_value = "aleatório"
            self.FIRST_TURN = False
        else:
            best_value = self.__minimax(deepcopy(self.TABLE), len(self.__get_rats_possible_moves()), -inf, inf, True)
            best_move = None
            for moves in self.__get_rats_possible_moves().items():
                if len(moves[1]) != 0:
                    value = self.__minimax(deepcopy(self.TABLE), len(self.__get_rats_possible_moves()) - 1, -inf, inf,
                                           False)
                    if value == best_value:
                        best_move = moves[1][0]

            x, y = best_move

        print(f"A IA fez a jogada ({x}, {y}) com o rato {map_y_to_rat(y)} com valor de {best_value}")
        self.__exec_move(x, y, map_y_to_rat(y))
        self.CURRENT_PLAYER = 2

    def play(self):
        """
        Função responsável por inicializar o jogo
        """
        clear_console()
        print_table(self.TABLE)

        while not self.WINNER:
            self.__make_human_move() if self.CURRENT_PLAYER == 2 else self.__make_ia_move()
            self.__check_win()

        print("O GATO VENCEU!!!") if self.WINNER == 2 else print("OS RATOS VENCERAM!!!")
