import pygame
from gameObject import BorderBlock, Rock, IceBlock, Goal
from settings import *
from maps import *

""""
Model a game map. Include a grid (2d array) of game 
objects' positions, the map's name, and the map size(w,h).
"""
class Map():
    def __init__(self, grid, name):
        self.grid = grid    # 2D array of objects on maps
        self.name = name
        self.size = (len(self.grid[0]), len(self.grid)) # width, height

def read_maps():
    map_list = []
    # construct map objects from map list
    for num in range(len(maps)):    # 'maps' is list of 2D arrays
        m = Map(maps[num], 'map'+str(num))
        map_list.append(m)
    
    return map_list

def create_map(game_map):
    rocks = pygame.sprite.Group()
    ice_blocks = pygame.sprite.Group()
    borders = pygame.sprite.Group()
    goals = pygame.sprite.Group()
    
    grid = game_map.grid
    for row in range(len(grid)):
        for col in range(len(grid[row])):
            coords = (col*BLOCK_SIZE, row*BLOCK_SIZE)   # calculate initial object coords
            if grid[row][col] == '#':    # rock
                rock = Rock(coords)     # create rock object
                rocks.add(rock)     # add to sprite group

            if grid[row][col] == 'I':    # ice block
                ice = IceBlock(coords)       # create ice block object
                ice_blocks.add(ice)     # add to sprite group

            if grid[row][col] == 'B':    # border blocks outside of puzzle
                borderBlock = BorderBlock(coords)
                borders.add(borderBlock)

            if grid[row][col] == 'G':    # goal space
                goal = Goal(coords)
                goals.add(goal)
    
    # add ice blocks' obstacles
    ice_blocks_list = ice_blocks.sprites()
    for i in range(len(ice_blocks)):
        ice_blocks.sprites()[i].add_obstacles(rocks, borders) 
        for j in range(len(ice_blocks_list)):
            # an ice block must not collide with itself
            ice1 = ice_blocks_list[j]
            ice2 = ice_blocks.sprites()[i]
            if ice1 is ice2:    # 'is' same as '==='
                pass
            else:
                ice_blocks.sprites()[j].add_ice_blocks(ice_blocks_list[i])

    # return sprite groups
    return rocks, ice_blocks, borders, goals

