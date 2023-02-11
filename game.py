from utils import clear_console, get_cat_possible_moves, print_table


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
        self.CURRENT_RATS_POSITION = [[1, 0], [1, 1], [1, 2], [1, 5], [1, 6], [1, 7]]

    def make_human_move(self) -> None:
        while True:
            print(
                f"Possíveis movimentos: \n{get_cat_possible_moves(self.TABLE, self.CURRENT_CAT_POSITION)}"
            )
            x, y = input("Digite as coordenadas (x,y) no tabuleiro: \n").split()
            x = int(x)
            y = int(y)

            if [x, y] in get_cat_possible_moves(self.TABLE, self.CURRENT_CAT_POSITION):
                previous_cat_x, previous_cat_y = self.CURRENT_CAT_POSITION
                self.TABLE[x][y] = self.CURRENT_PLAYER
                self.TABLE[previous_cat_x][previous_cat_y] = 0
                self.CURRENT_CAT_POSITION = [x, y]
                self.CURRENT_PLAYER = 1
                break
            else:
                clear_console()
                print_table(self.TABLE)
                print("Movimento inválido!\n")
