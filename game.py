"""
@author: Filipe Augusto, Pedro Augusto
"""

"""
Módulo core para executar o Jogo do gato e dos ratos.
"""

from utils import clear_console, get_user_input, print_table, get_cat_x_path, get_cat_y_path
from math import inf
from copy import deepcopy
from random import choice


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
        self.ALIVE_RATS = 6
        self.CURRENT_RATS_POSITION = {
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

    def __get_rats_possible_moves(self) -> dict:
        """
        Função que retorna os possíveis movimentos para cada rato vivo
        :return: Dicionário com movimentos possíveis para cada rato
        """
        cells = {0: None, 1: None, 2: None, 3: None, 4: None, 5: None}

        for rat, position in self.CURRENT_RATS_POSITION.items():
            rat_x, rat_y = position

            if rat_x == inf:
                current_rat_moves = [[inf, inf]]
            else:
                current_rat_moves = [[rat_x + 1, rat_y]] if self.TABLE[rat_x + 1][rat_y] == 0 else [[inf, inf]]



            if self.CURRENT_RATS_MOVES_COUNT[rat] == 0:
                current_rat_moves.append([rat_x + 2, rat_y])
                cells[rat] = current_rat_moves
            else:
                cells[rat] = current_rat_moves

        return cells

    def __get_cat_possible_moves(self):
        """
        Função que retorna uma lista de movimentos possíveis para o jogador humano
        :return: Lista de movimentos possíveis para o gato
        """
        x_axis_moves = get_cat_x_path(self.TABLE, self.CURRENT_CAT_POSITION)
        y_axis_moves = get_cat_y_path(self.TABLE, self.CURRENT_CAT_POSITION)
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
                self.CURRENT_RATS_POSITION[self.__map_y_to_rat(y)] = [inf, inf]
            self.TABLE[previous_cat_x][previous_cat_y] = 0
            self.TABLE[x][y] = self.CURRENT_PLAYER
            self.CURRENT_CAT_POSITION = [x, y]
            self.CURRENT_PLAYER = 1
            clear_console()
            print_table(self.TABLE)
        else:
            previous_rat_x, previous_rat_y = self.CURRENT_RATS_POSITION[rat]
            self.TABLE[x][y] = self.CURRENT_PLAYER
            self.TABLE[previous_rat_x][previous_rat_y] = 0
            self.CURRENT_RATS_POSITION[rat] = [x, y]
            self.CURRENT_RATS_MOVES_COUNT[rat] += 1
            self.CURRENT_PLAYER = 2
            clear_console()
            print_table(self.TABLE)

    def __eval(self, copy: list[list[int] | None]):
        alive_rats = 0
        cat_position = None
        rats_position = {0: [None, None], 1: [None, None], 2: [None, None], 3: [None, None], 4: [None, None], 5: [None, None]}
        for cell in copy[7]:
            if cell == 1:
                return 1

        for line in range(len(copy)):
            for column in range(len(copy[line])):
                if copy[line][column] == 1:
                    alive_rats += 1
                    rats_position[self.__map_y_to_rat(column)] = [line][column]

                if copy[line][column] == 2:
                    cat_position = copy[line][column]

            if alive_rats == 0:
                return -1

            cat_x, cat_y = cat_position
            for _, position in rats_position.items():
                rat_x, rat_y = position
                if rat_x == cat_x - 1 and (rat_y == cat_y + 1 and rat_y == cat_y - 1):
                    return 1

            return 0

    def __minimax(self, state: list[list[int]], depth: int, player: int):
        if player == 1:
            best_value = [-1, -1, -inf]
        else:
            best_value = [-1, -1, +inf]

        if depth == 0  or self.__check_win():
            if self.WINNER == None:
                score = 0
            elif self.WINNER == 1:
                score = 1
            else:
                score = 2
            return [-1, -1, score]

        if player == 1:
            for rat, _ in self.CURRENT_RATS_POSITION.items():
                for cell in self.__get_rats_possible_moves()[rat]:
                    x, y = cell
                    if x == inf or y == inf:
                        break
                    state[x][y] = player
                    score = self.__minimax(state, depth - 1, 2)
                    state[x][y] = 0
                    score[0], score[1] = x, y

                    if player == 1:
                        if score[2] > best_value[2]:
                            best_value = score
                    else:
                        if score[2] < best_value[2]:
                            best_value = score

        else:
            for move in self.__get_cat_possible_moves():
                x, y = move
                state[x][y] = player
                score = self.__minimax(state, depth - 1, 1)
                state[x][y] = 0
                score[0], score[1] = x, y

                if player == 1:
                    if score[2] > best_value[2]:
                        best_value = score
                else:
                    if score[2] < best_value[2]:
                        best_value = score

        return best_value


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

    def __map_y_to_rat(self, y):
        if y <= 2:
            return y
        if y == 5:
            return 3
        if y == 6:
            return 4
        if y == 7:
            return 5

    def __make_ia_move(self) -> None:
        """
        Função que executa o algoritmo MINMAX e realiza o movimento da IA
        :return: Tabuleiro atualizado com novas posições
        """
        print("IA pensando ...")

        if self.FIRST_TURN:
            x, y = choice(choice(self.__get_rats_possible_moves()))
            self.FIRST_TURN = False
        else:
            x, y, _ = self.__minimax(deepcopy(self.TABLE), len(self.__get_rats_possible_moves()), 1)

        print(f"A IA fez a jogada ({x}, {y}) com o rato {self.__map_y_to_rat(y)}")
        self.__exec_move(x, y, self.__map_y_to_rat(y))
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
