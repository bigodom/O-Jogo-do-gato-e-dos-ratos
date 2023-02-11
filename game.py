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
        self.CURRENT_RATS_POSITION = [[1, 0], [1, 1], [1, 2], [1, 5], [1, 6], [1, 7]]
        self.CURRENT_RATS_MOVES_COUNT = [0, 0, 0, 0, 0, 0]

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

    def __exec_move(self, x: int, y: int, rat: int | None = None) -> None:
        if self.CURRENT_PLAYER == 2:
            previous_cat_x, previous_cat_y = self.CURRENT_CAT_POSITION
            self.TABLE[x][y] = self.CURRENT_PLAYER
            self.TABLE[previous_cat_x][previous_cat_y] = 0
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
