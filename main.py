from gui import *


def start_player_game():
    game, font, clock, screen, main_menu, load_level_menu = init_gui()
    start_main_menu(game, font, clock, screen, main_menu, load_level_menu)


## Create Data
def run_ai_game_and_return_data(level, heuristic, is_goal_func):
    game, font, clock, screen, main_menu, load_level_menu = init_gui()
    game.is_ai = True
    return start_level(level, game, font, clock, screen, main_menu, load_level_menu, heuristic=heuristic, calc_stats=True, is_goal_func=is_goal_func)


## NN
def start_nn_game(level):
    game, font, clock, screen, main_menu, load_level_menu = init_gui()
    return start_nn_level(level, game, font, clock, screen, main_menu, load_level_menu)


def start_nn_game_without_gui(level):
    game = Game()
    game.is_ai = True
    game.is_nn = True
    game.load_level(level)
    return game


def start_nn_level(level, game, font, clock, screen, main_menu, load_level_menu):
    game.is_ai = True
    game.is_nn = True
    game.load_level(level)
    main_menu.is_active = False
    pygame.mouse.set_visible(False)
    return game, font, clock, screen, main_menu, load_level_menu

if __name__ == '__main__':
    start_player_game()

