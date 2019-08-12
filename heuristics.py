import math
from settings import *
from a_star_utils import *
import numpy as np


DANGER_DIST_FROM_BUBBLE = 290
DANGER_X_DIST_FROM_BUBBLE = 40
DANGER_Y_DIST_FROM_BUBBLE = 80
DANGER_TIME_FROM_BUBBLE = 8
X_TOO_FAR_FOR_SHOOTING = 100

# heuristics:

def stay_in_ball_area_but_not_too_close_heuristic_time_admissible(game, start):
    if not game.balls and not game.hexagons:
        return 0
    time_to_closest_bubble = get_time_to_closest_bubble(game)
    if time_to_closest_bubble < DANGER_TIME_FROM_BUBBLE:
            return (DANGER_TIME_FROM_BUBBLE-time_to_closest_bubble) * 1000
    elif is_sub_goal_score_or_steps(game, start):
        return 0
    return time_to_closest_bubble * 5


def stay_in_ball_area_but_not_too_close_x_axis_not_admissible_heuristic(game, start):
    if not game.balls and not game.hexagons:
        return 0
    agent_dist = find_the_distance_from_the_closest_ball_at_x_axis(game)[1]
    if agent_dist < DANGER_X_DIST_FROM_BUBBLE:
        return (DANGER_X_DIST_FROM_BUBBLE - agent_dist) * 1000
    elif is_sub_goal_score_or_steps(game, start):
        return 0
    return agent_dist


def stay_in_ball_area_but_not_too_close_both_axis_not_admissible_heuristic(game, start):
    if not game.balls and not game.hexagons:
        return 0
    close_bubble, agent_dist = find_the_distance_from_the_closest_bubble(game)
    if agent_dist < DANGER_DIST_FROM_BUBBLE:
            return (DANGER_DIST_FROM_BUBBLE - agent_dist) * 1000
    elif is_sub_goal_score_or_steps(game, start):
        return 0
    return agent_dist


def bonus_and_ball_but_not_too_close_heuristic(game, start):
    if not game.balls and not game.hexagons:
        return 0
    agent_dist = find_the_distance_from_the_closest_bubble(game)[1]
    agent_x_dist = find_the_distance_from_the_closest_ball_at_x_axis(game)[1]
    if agent_dist < DANGER_DIST_FROM_BUBBLE and agent_x_dist < DANGER_X_DIST_FROM_BUBBLE:
        return (DANGER_DIST_FROM_BUBBLE-agent_dist) * 1000
    elif is_sub_goal_score_or_steps(game, start):
        return 0
    dist_from_bonus = pick_up_bonuses(game)
    return min(dist_from_bonus, agent_dist)


def stay_in_center_heuristic(game, start):
    if not game.balls and not game.hexagons:
        return 0
    agent_dist = find_the_distance_from_the_closest_bubble(game)[1]
    agent_x_dist = find_the_distance_from_the_closest_ball_at_x_axis(game)[1]
    if agent_dist < DANGER_DIST_FROM_BUBBLE and agent_x_dist < DANGER_X_DIST_FROM_BUBBLE:
        return (DANGER_DIST_FROM_BUBBLE - agent_dist) * 1000
    elif is_sub_goal_score_or_steps(game, start):
        return 0
    x_center = WINDOWWIDTH // 2
    return abs(game.players[0].rect.centerx - x_center)


def shoot_on_small_balls_heuristic(game, start):
    if not game.balls and not game.hexagons:
        return 0
    agent_dist_from_smallest_ball = find_the_distance_from_the_closest_smallest_ball_x_axis(game)[1]
    agent_dist_from_closest_ball = find_the_distance_from_the_closest_ball_at_x_axis(game)[1]
    if agent_dist_from_closest_ball < DANGER_X_DIST_FROM_BUBBLE:
        return (DANGER_X_DIST_FROM_BUBBLE - agent_dist_from_closest_ball) * 1000
    elif game.players[0].weapon.is_active:
        dist_from_weapon_to_smallest_close_ball = distance_from_weapon_and_smallest_bubbles(game)
        if dist_from_weapon_to_smallest_close_ball > X_TOO_FAR_FOR_SHOOTING:
            return (dist_from_weapon_to_smallest_close_ball + agent_dist_from_smallest_ball) / 3
    elif is_sub_goal_score_or_steps(game, start):
        return 0
    return agent_dist_from_smallest_ball / 3


# TODO if we want....
def shoot_heuristic(game, starting_score, path_size):
    if len(game.balls) == 0 and len(game.hexagons) == 0:
        return 0
    ball, distance_from_closest_ball = find_the_distance_from_the_closest_ball_at_x_axis(game)
    if distance_from_closest_ball < 70 and game.players[0].weapon.is_active:
        return -(70-distance_from_closest_ball)
    elif distance_from_closest_ball >= 70 and game.players[0].weapon.is_active:
        return distance_from_closest_ball
    return 0


def zero_heuristic(game, start):
    return 0

# Helper functions

def distance_from_weapon_and_smallest_bubbles(game):
    bubbles = game.balls + game.hexagons
    min_size = min([bubble.size for bubble in bubbles])
    small_bubbles = [bubble for bubble in bubbles if bubble.size == min_size]
    return distance_from_weapon_and_bubbles_list(game, small_bubbles)


def distance_from_weapon_and_bubble(game):
    if game.players[0].weapon.is_active:
        return distance_from_weapon_and_bubbles_list(game, game.balls + game.hexagons)
    return WINDOWWIDTH


def distance_from_weapon_and_bubbles_list(game, bubbles_list):
    return min([abs(bubble.rect.centerx - game.players[0].weapon.rect.centerx) for bubble in bubbles_list])


def find_the_distance_from_the_closest_ball_at_x_axis(game, index = 0):
    bubbles = game.balls + game.hexagons
    return find_x_axis_closest_bubble_from_list(game, bubbles)

#
# def distance_between_ball_and_player(ball, game, index = 0):
#     distance_x = ball.rect.centerx - game.players[index].rect.centerx
#     distance_y = ball.rect.centery - game.players[index].rect.bottom
#     return math.sqrt(math.pow(distance_x, 2) + math.pow(distance_y, 2))


def distance_between_bonus_and_player(bonus, game, index = 0):
    distance = abs(bonus.rect.centerx - game.players[index].rect.centerx)
    return distance


def distance_sign_between_ball_and_player(ball,game,index=0):
    return ball.rect.centerx - game.players[index].rect.centerx


def find_the_distance_from_the_closest_bubble(game, index = 0):
    bubbles = game.balls + game.hexagons
    return find_euclidian_closest_bubble_from_list(game, bubbles)


def find_euclidian_closest_bubble_from_list(game, bubbles_list):
    bubbles_dist = [euclidean_dist_bubble_and_player(bubble, game.players[0]) for bubble in bubbles_list]
    min_dist_bubble_index = int(np.argmin(np.array(bubbles_dist)))
    return bubbles_list[min_dist_bubble_index], bubbles_dist[min_dist_bubble_index]


def find_x_axis_closest_bubble_from_list(game, bubbles_list):
    bubbles_dist = [dist_from_bubble_and_player(bubble, game.players[0], axis=0) for bubble in bubbles_list]
    min_dist_bubble_index = int(np.argmin(np.array(bubbles_dist)))
    return bubbles_list[min_dist_bubble_index], bubbles_dist[min_dist_bubble_index]


def find_the_distance_from_the_closest_smallest_ball_x_axis(game):
    bubbles = game.balls + game.hexagons
    min_size = min([bubble.size for bubble in bubbles])
    small_bubbles = [bubble for bubble in bubbles if bubble.size == min_size]
    return find_x_axis_closest_bubble_from_list(game, small_bubbles)


def find_the_distance_from_the_closest_smallest_ball(game):
    bubbles = game.balls + game.hexagons
    min_size = min([bubble.size for bubble in bubbles])
    small_bubbles = [bubble for bubble in bubbles if bubble.size == min_size]
    return find_euclidian_closest_bubble_from_list(game, small_bubbles)


def time_from_bubble_and_player(game, bubble, axis=0, player_index=0):
    dist_from_bubble = dist_from_bubble_and_player(bubble, game.players[0], axis)
    bubble_axis_speed = abs(bubble.speed[axis])
    if axis == 0:
        total_speed = max(PLAYER_SPEED + bubble_axis_speed, 1)
    else:
        if bubble.image_name == BALL_IMAGE_NAME:
            # TODO: it's for addmissable
            total_speed = max(bubble_axis_speed + 2 * np.sqrt(dist_from_bubble), 1)
        else:
            total_speed = max(bubble_axis_speed, 1)
    time_from_bubble = int(np.ceil(dist_from_bubble / total_speed))
    return time_from_bubble


def dist_from_bubble_and_player(bubble, player, axis=0):
    if axis == 0:
        player_spot = player.rect.centerx
        pos_bubble_spot = bubble.rect.left
        neg_bubble_spot = bubble.rect.right
        return min(abs(player_spot - pos_bubble_spot), abs(player_spot - neg_bubble_spot))
    else:
        return abs(bubble.rect.bottom)


def euclidean_dist_bubble_and_player(bubble, player):
    return math.sqrt(math.pow(dist_from_bubble_and_player(bubble, player, 0),2) + math.pow(dist_from_bubble_and_player(bubble, player, 1),2))


def get_time_to_closest_bubble(game, player_index=0):
    closest_bubble = None
    dist_from_closest_bubble = None
    for cur_bubble in game.balls + game.hexagons:
        cur_bubble_dist = euclidean_dist_bubble_and_player(cur_bubble, game.players[player_index])
        if not closest_bubble or cur_bubble_dist < dist_from_closest_bubble:
            closest_bubble = cur_bubble
            dist_from_closest_bubble = cur_bubble_dist
    return max(time_from_bubble_and_player(game, closest_bubble, 0, player_index),
               time_from_bubble_and_player(game, closest_bubble, 1, player_index))


def time_from_closest_bubble_at_axis(game, axis=0, player_index=0):
    if len(game.balls) != 0:
        cur_bubble = game.balls[0]
        time_from_closest_bubble = time_from_bubble_and_player(game, cur_bubble, axis, player_index)
        closest_bubble = cur_bubble
    else:
        cur_bubble = game.hexagons[0]
        time_from_closest_bubble = time_from_bubble_and_player(game, cur_bubble, axis, player_index)
        closest_bubble = cur_bubble
    for i in range(1, len(game.balls)):
        cur_bubble = game.balls[i]
        time_from_bubble = time_from_bubble_and_player(game, cur_bubble, axis, player_index)
        if time_from_bubble < time_from_closest_bubble:
            time_from_closest_bubble = time_from_bubble
            closest_bubble = cur_bubble
    for i in range(1, len(game.hexagons)):
        cur_bubble = game.hexagons[i]
        time_from_bubble = time_from_bubble_and_player(game, cur_bubble, axis, player_index)
        if time_from_bubble < time_from_closest_bubble:
            time_from_closest_bubble = time_from_bubble
            closest_bubble = cur_bubble
    return closest_bubble, time_from_closest_bubble


def pick_up_bonuses(game):
    distance_from_closest_bonus = WINDOWWIDTH + 1
    if len(game.bonuses) == 0:
        return distance_from_closest_bonus
    for bonus in game.bonuses:
        if bonus.rect.centery > 20:
            continue
        else:
            distance_from_bonus = distance_between_bonus_and_player(bonus, game)
        if distance_from_bonus < distance_from_closest_bonus:
            distance_from_closest_bonus = distance_from_bonus
    return distance_from_closest_bonus

