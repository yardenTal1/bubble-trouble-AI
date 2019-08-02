import os

## General fields
WINDOWWIDTH = 640
WINDOWHEIGHT = 480
FPS = 30
WEAPON_SPEED = 15
PLAYER_SPEED = 5
BONUS_SPEED = 2
BONUS_DROP_RATE = 10
WHITE = (255, 255, 255)
RED = (255, 0, 0)
PURPLE = (100, 25, 180)
BLUE = (0, 0, 200)
BLACK = (0, 0, 0)
GRAVITY = 1
STARTING_LIVES = 3
MAX_LEVEL = 8

RUN_LOCAL = True
if RUN_LOCAL:
    APP_PATH = os.path.dirname(__file__) + '/'
    IMAGES_PATH = APP_PATH + 'images/'
    SHOW_NN_GUI = False
    PLAY_BY_MYSELF = False
else:
    APP_PATH = os.path.dirname(__file__) + '/content/'
    IMAGES_PATH = APP_PATH
    SHOW_NN_GUI = False
    PLAY_BY_MYSELF = False

## AI fields
AI_PLAYER_NUM = 0
MOVE_LEFT = 'left'
MOVE_RIGHT = 'right'
STAY = 'stay'
SHOOT = 'shoot'
A_STAR_ACTION_LIST = [MOVE_LEFT, MOVE_RIGHT, SHOOT]
NN_ACTION_LIST = [MOVE_LEFT, MOVE_RIGHT, SHOOT]
ACTIONS_LEN = len(NN_ACTION_LIST)

# AI - astar fields
LOOP_AT_EACH_MOVE_UPDATE = 3
MAX_VISITED_LEN = 300
MAX_PATH_SIZE = 8

# NN fields
BALLS_AT_STATE = 5
EACH_BALL_REPR = 5
GENERAL_REPR = 3
STATE_LEN = (BALLS_AT_STATE*EACH_BALL_REPR) + GENERAL_REPR
EPISODES = 1000
