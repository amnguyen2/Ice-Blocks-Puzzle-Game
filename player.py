import pygame
from settings import *

"""
Player moves around the map, controlled by user. Player can move Ice Blocks 
by colliding with them and pressing movement keys. Ice Blocks move in the same 
direction that the Player is moving, as long as Player is 'behind' that Ice Block.
"""
class Player(pygame.sprite.Sprite):
    def __init__(self, pos, obstacles, ice, bounds):
        super().__init__()

        self.image = pygame.Surface([PLAYER_SIZE, PLAYER_SIZE])
        self.image.fill(PLAYER_COLOR)
        self.rect = self.image.get_rect(topleft = pos)

        self.pos = pos
        self.direction = pygame.math.Vector2()  # x, y
        self.obstacles = obstacles
        self.ice_blocks = ice
        self.bounds = bounds    # where player is allowed to go on screen

        self.speed = PLAYER_SPEED
        

    def input(self):
        keys = pygame.key.get_pressed()

        if keys[pygame.K_UP]: # up = -y
            self.direction.y = -1
        elif keys[pygame.K_DOWN]: # down = +y
            self.direction.y = 1
        else:
            self.direction.y = 0

        if keys[pygame.K_RIGHT]: # right = +x
            self.direction.x = 1
        elif keys[pygame.K_LEFT]: # left = -x
            self.direction.x = -1
        else:
            self.direction.x = 0


    def move(self, speed):
        if self.direction.magnitude() != 0:
            self.direction = self.direction.normalize()

        self.rect.x += self.direction.x * speed
        self.collision('horizontal')
        self.rect.y += self.direction.y * speed
        self.collision('vertical')


    def collision(self, direction):
        if direction == 'horizontal':
            # screen area
            if self.rect.right > self.bounds[0]: # right
                self.rect.right = self.bounds[0]
            elif self.rect.left < 0: # left
                self.rect.left = 0
            
            for sprite in self.obstacles:   # obstacles
                if sprite.rect.colliderect(self.rect):
                    if self.direction.x > 0: # moving right
                        self.rect.right = sprite.rect.left
                    elif self.direction.x < 0: # moving left
                        self.rect.left = sprite.rect.right

            for sprite in self.ice_blocks:  # ice blocks
                if sprite.rect.colliderect(self.rect): # if collide with ice
                    if (self.direction.x > 0): # moving right
                        self.rect.right = sprite.rect.left 
                        sprite.move([1, 0], ICE_BLOCK_SPEED) # move ice right

                    elif (self.direction.x < 0): # moving left
                        self.rect.left = sprite.rect.right
                        sprite.move([-1, 0], ICE_BLOCK_SPEED) # move ice left

        if direction == 'vertical':
            # screen area
            if self.rect.bottom > self.bounds[1]: # down
                self.rect.bottom = self.bounds[1]
            elif self.rect.top < 0: # up
                self.rect.top = 0

            for sprite in self.obstacles:   # obstacles
                if sprite.rect.colliderect(self.rect):
                    if self.direction.y > 0: # moving down
                        self.rect.bottom = sprite.rect.top
                    elif self.direction.y < 0: # moving up
                        self.rect.top = sprite.rect.bottom

            for sprite in self.ice_blocks:  # ice blocks
                if sprite.rect.colliderect(self.rect): # if collide with ice
                    if (self.direction.y > 0): # moving down
                        self.rect.bottom = sprite.rect.top
                        sprite.move([0, 1], ICE_BLOCK_SPEED) # move ice down
                 
                    elif (self.direction.y < 0): # moving up
                        self.rect.top = sprite.rect.bottom
                        sprite.move([0, -1], ICE_BLOCK_SPEED) # move ice up
                  

    def update(self):
        self.input()
        self.move(self.speed)
        
        
        