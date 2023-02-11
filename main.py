from game import Game
from utils import print_table

if __name__ == "__main__":
    game = Game()
    print_table(game.TABLE)
    game.make_human_move()  # Atualmente o humano está começando, mudar depois.
