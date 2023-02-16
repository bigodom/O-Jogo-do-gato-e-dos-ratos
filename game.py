from utils import clear_console, get_cat_possible_moves, get_user_input, print_table


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
        self.CURRENT_PLAYER = 2
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

    def make_human_move(self) -> None:
        possible_cat_moves = get_cat_possible_moves(
            self.TABLE, self.CURRENT_CAT_POSITION
        )

        while True:
            print(f"Possíveis movimentos: \n{possible_cat_moves}\n")
            x, y = get_user_input()

            if [x, y] in possible_cat_moves:
                self.__exec_move(x, y)
                break
            else:
                clear_console()
                print_table(self.TABLE)
                print("Movimento inválido!\n")

    def __get_rats_possible_move(self) -> list[list[int, int]]:
        cells = {0: None, 1: None, 2: None, 3: None, 4: None, 5: None}

        for rat, position in self.CURRENT_RATS_POSITION.items():
            rat_x, rat_y = position
            current_rat_moves = [[rat_x + 1, rat_y]]

            if rat_x == float("inf"):
                current_rat_moves = [[float("inf"), float("inf")]]

            if self.CURRENT_RATS_MOVES_COUNT[rat] == 0:
                current_rat_moves.append([rat_x + 2, rat_y])
                cells[rat] = current_rat_moves
            else:
                cells[rat] = current_rat_moves

        return cells

    def __exec_move(self, x: int, y: int, rat: int | None = None) -> None:
        if self.CURRENT_PLAYER == 2:
            previous_cat_x, previous_cat_y = self.CURRENT_CAT_POSITION
            if self.TABLE[x][y] == 1:
                self.ALIVE_RATS -= 1
                self.CURRENT_RATS_POSITION[x] = [float("inf"), float("inf")]
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

    def __check_win(self) -> list[bool, int] | bool:
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
            if rat_x == cat_x - 1 and (rat_y == cat_y + 1 or rat_y == cat_y - 1):
                self.WINNER = 1
                return [True, 1]

        return False

    def make_ia_move(self) -> None:
        print("IA VEZ MOCK")
        print(f"Movimentos dos ratos: {self.__get_rats_possible_move()}")
        self.CURRENT_PLAYER = 2

    def play(self):
        clear_console()
        print_table(self.TABLE)

        while not self.WINNER:
            self.make_human_move() if self.CURRENT_PLAYER == 2 else self.make_ia_move()
            self.__check_win()

        print("O GATO VENCEU!!!") if self.WINNER == 2 else print("OS RATOS VENCERAM!!!")
