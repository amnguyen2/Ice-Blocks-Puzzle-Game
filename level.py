import pygame
from player import Player
from map import create_map
from settings import * 

"""
Model all game objects (player, obstacles, ice blocks, goals, borders) 
together as a 'package'
"""
class Level():
    def __init__(self):
        self.stiff_sprites = pygame.sprite.Group() 
        self.goal_sprites = pygame.sprite.Group()
        self.player_sprite = pygame.sprite.Group()
        self.ice_sprites = pygame.sprite.Group()

    def setup(self, game_map):
        rocks, ice_blocks, borders, goals = create_map(game_map)
        self.stiff_sprites.add(rocks, borders)
        self.goal_sprites.add(goals)

        # create player
        pos = ((game_map.size[0]*BLOCK_SIZE/2)-(PLAYER_SIZE/2), 10)
        bounds = (game_map.size[0]*BLOCK_SIZE, game_map.size[1]*BLOCK_SIZE)
        player = Player(pos, rocks, ice_blocks, (bounds))
        self.player_sprite.add(player)
        self.ice_sprites.add(ice_blocks)

    def check_win(self):
        for goal in self.goal_sprites:   # check all goals
            goal_met = goal.check_goal(self.ice_sprites)     # check if any ice is on goal
            if goal_met == False:   # if one goal has not been met
                return False
        return True     # all goals met