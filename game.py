from copy import deepcopy
from math import inf
from random import choice

from utils import clear_console, get_user_input, print_table, get_cat_x_path, get_cat_y_path, map_y_to_rat, \
    max_heuristic, is_end_state, get_rats_possible_moves_from_state, min_heuristic

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
                del self.CURRENT_RATS_POSITION[map_y_to_rat(y)]
                del self.MAX_RATS_POSITION[map_y_to_rat(y)]
            self.TABLE[previous_cat_x][previous_cat_y] = 0
            self.TABLE[x][y] = self.CURRENT_PLAYER
            self.CURRENT_CAT_POSITION = [x, y]
            self.MIN_CAT_POSITION = [x, y]
            self.CURRENT_PLAYER = 1
            clear_console()
            print_table(self.TABLE)
        else:
            previous_rat_x, previous_rat_y = self.CURRENT_RATS_POSITION[rat]
            if self.TABLE[x][y] == 2:
                self.CURRENT_CAT_POSITION = None
            self.TABLE[x][y] = self.CURRENT_PLAYER
            self.TABLE[previous_rat_x][previous_rat_y] = 0
            self.CURRENT_RATS_POSITION[rat] = [x, y]
            self.MAX_RATS_POSITION[rat] = [x, y]
            self.MAX_RATS_MOVES_COUNT[rat] += 1
            self.CURRENT_RATS_MOVES_COUNT[rat] += 1
            self.CURRENT_PLAYER = 2
            clear_console()
            print_table(self.TABLE)

    def __eval(self, state: list[list[int] | None], max_player: bool):
        """
        Função de avaliação de estado
        :param state: Estado atual
        :param max_player: Indetificador se é o jogador MAX ou MIN
        :return: Valor de avaliação do estado se for um estado final, se não avaliação heuristica
        """
        is_end, value = is_end_state(state)

        if is_end:
            return value
        if max_player:
            return max_heuristic(state)
        else:
            return min_heuristic(state)

    def __exec_max_move(self, state: list[list[int]], x: int, y: int, rat: int):
        """
        Executa movimento MAX no estado atual do minimax
        :param state: Estado atual
        :param x: Linha do tabuleiro
        :param y: Coluna do tabuleiro
        :param rat: Rato escolhido
        :return: Estado atualizado
        """
        previous_x, previous_y = self.MAX_RATS_POSITION[rat]
        if previous_x != inf:
            state[previous_x][previous_y] = 0
            state[x][y] = 1
            self.MAX_RATS_POSITION[rat] = [x, y]
            self.MAX_RATS_MOVES_COUNT[rat] += 1

    def __undo_max_move(self, state: list[list[int]], x: int, y: int, rat: int):
        """
        Desfaz o movimento no estado atual, necessário para subir na árvore
        :param state: Estado atual
        :param x: Linha do tabuleiro
        :param y: Coluna do tabuleiro
        :param rat: Rato escolhido
        :return: Estado atualizado
        """
        if x == inf or y == inf:
            return
        actual_x, actual_y = self.MAX_RATS_POSITION[rat]
        if actual_x == inf or actual_y == inf:
            state[x - 1][y] = 0

        else:
            state[actual_x][actual_y] = 0
        if state[x][y] == 2:
            self.MIN_CAT_POSITION = None
        state[x][y] = 1
        self.MAX_RATS_POSITION[rat] = [x, y]
        self.MAX_RATS_MOVES_COUNT[rat] -= 1

    def __exec_min_move(self, state: list[list[int]], x: int, y: int):
        """
        Executa movimento MIN no estado atual do minimax
        :param state: Estado atual do minimax
        :param x: Linha no tabuleiro
        :param y: Coluna no tabuleiro
        :return: Estado atualizado
        """
        previous_x, previous_y = self.MIN_CAT_POSITION
        if state[x][y] == 1:
            self.MAX_ALIVE_RATS -= 1
            self.MAX_RATS_POSITION[map_y_to_rat(y)] = [inf, inf]
        state[previous_x][previous_y] = 0
        state[x][y] = 2
        self.MIN_CAT_POSITION = [x, y]

    def undo_min_move(self, state: list[list[int]], x: int, y: int):
        """
        Desfaz movimento MIN no estado atual do minimax, necessário para subir na árvore
        :param state: Estado atual do minimax
        :param x: Linha do tabuleiro
        :param y: Coluna do tabuleiro
        :return: Estado atualizado
        """
        actual_x, actual_y = self.MIN_CAT_POSITION
        if state[x][y] == 1:
            self.MAX_ALIVE_RATS -= 1
            self.MAX_RATS_POSITION[map_y_to_rat(y)] = [inf, inf]
        state[actual_x][actual_y] = 0
        state[x][y] = 2
        self.MIN_CAT_POSITION = [x, y]

    def __get_rats_max_possible_moves(self, state: list[list[int]]):
        """
        Obtem movimentos dos ratos no estado atual (MAX)
        :param state: Estado atual MAX
        :return: Movimentos dos ratos no estado atual
        """
        moves = []
        for rat, position in self.MAX_RATS_POSITION.items():
            if rat:
                for cell in self.__get_rats_possible_moves(is_max=True, copy=state)[rat]:
                    x, y = cell
                    if x != inf and y != inf:
                        moves.append([rat, x, y])

        return moves

    def __minimax(self, state: list[list[int]], depth: int, max_player: bool):
        """
        Algoritmo MINIMAX para obter a melhor jogada (IA)
        :param state: Estado atual
        :param depth: Profundidade da árvore
        :param max_player: Identificador se é o jogador MAX ou jogador MIN
        :return: Melhor movimento e seu custo heurístico
        """

        if is_end_state(state)[0] or depth == 0:
            utility = self.__eval(state, max_player)
            return utility, None

        if max_player:
            best_move = None
            max_eval = -inf
            actions = get_rats_possible_moves_from_state(state)
            for action in actions:
                rat, x, y = action
                undo_x, undo_y = self.MAX_RATS_POSITION[rat]
                self.__exec_max_move(state, x, y, rat)
                current_eval, _ = self.__minimax(state, depth - 1, False)
                self.__undo_max_move(state, undo_x, undo_y, rat)
                if current_eval < max_eval or best_move is None:
                    max_eval = current_eval
                    best_move = [x, y]
            return max_eval, best_move

        else:
            best_move = None
            min_eval = inf
            for move in self.__get_cat_possible_moves(state):
                x, y = move
                undo_x, undo_y = self.MIN_CAT_POSITION
                self.__exec_min_move(state, x, y)
                current_eval, _ = self.__minimax(state, depth - 1, True)
                self.undo_min_move(state, undo_x, undo_y)
                if current_eval > min_eval or best_move is None:
                    min_eval = current_eval
                    best_move = [x, y]
            return min_eval, best_move

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

        cat = self.CURRENT_CAT_POSITION
        if not cat:
            self.WINNER = 1
            return [True, 1]
        else:
            cat_x, cat_y = cat

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
            x, y = choice(choice(self.__get_rats_possible_moves()))
            value = "aleatório"
            self.FIRST_TURN = False
        else:
            value, move = self.__minimax(deepcopy(self.TABLE), self.ALIVE_RATS, True)
            if move is None:
                print("OS RATOS IRÃO PERDER! A IA não possui movimentos!")
                self.WINNER = 2
                return
            print(f"RETORNO MINIMAX: {move}. valor da jogada: {value}")
            x, y = move

        if map_y_to_rat(y) not in self.CURRENT_RATS_POSITION:
            if map_y_to_rat(y - 1) in self.CURRENT_RATS_POSITION == x:
                rat = map_y_to_rat(y - 1)
            else:
                rat = map_y_to_rat(y + 1)
        else:
            rat = map_y_to_rat(y)
        print(f"A IA fez a jogada ({x}, {y}) com o rato {rat} com valor heruístico = {value}")
        self.__exec_move(x, y, rat)
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
