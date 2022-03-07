import pygame
from settings import * 
"""
Border Blocks frame each map. Player can move 
on this surface, but block Ice Blocks' movement.
"""
class BorderBlock(pygame.sprite.Sprite):
    def __init__(self, pos):
        super().__init__()

        self.image = pygame.Surface([BLOCK_SIZE, BLOCK_SIZE])
        self.image.fill(BORDER_COLOR)
        self.rect = self.image.get_rect(topleft = pos)

"""
Rocks block movement from both Player and Ice Block.
"""
class Rock(pygame.sprite.Sprite):
    def __init__(self, pos):
        super().__init__()

        self.image = pygame.Surface([BLOCK_SIZE, BLOCK_SIZE])
        self.image.fill(STONE_GRAY)
        self.rect = self.image.get_rect(topleft = pos)

"""
Goal represents a win condition. Player completes a map 
once every goal is covered by an Ice Block.
"""
class Goal(pygame.sprite.Sprite):
    def __init__(self, pos):
        super().__init__()
        spill = 4
        pos = (pos[0]-spill, pos[1]-spill)
        self.image = pygame.Surface([BLOCK_SIZE+(spill*2), BLOCK_SIZE+(spill*2)])
        self.image.fill(GOAL_COLOR)
        self.rect = self.image.get_rect(topleft = pos)
        
        pygame.draw.rect(self.image, WIN_RECT_COLOR, [0, 0, BLOCK_SIZE+(spill*2), BLOCK_SIZE+(spill*2)], 4)

    def check_goal(self, ice_blocks):
        for ice in ice_blocks:  # check if any ice block is on this goal
            if (self.rect.centerx == ice.rect.centerx) and (self.rect.centery == ice.rect.centery):
                return True 
        return False

    def update(self, ice_blocks):
        self.check_goal(ice_blocks)

"""
Ice Blocks can be pushed by Player. Once Player moves into an Ice Block, 
the Ice Block moves in the direction opposite the Player until it collides with
a Rock, Border Block, or another Ice Block. 
"""
class IceBlock(pygame.sprite.Sprite):
    def __init__(self, pos, obstacles=None, ice=None):
        super().__init__()

        self.image = pygame.Surface([BLOCK_SIZE, BLOCK_SIZE])
        self.image.fill(ICE_BLUE)
        self.rect = self.image.get_rect(topleft = pos)

        self.direction = pygame.math.Vector2()  # x, y
        self.obstacles = pygame.sprite.Group()
        self.ice_blocks = pygame.sprite.Group()
        
        if ice is not None:
            self.ice_blocks.add(ice)
        if obstacles is not None:
            self.obstacles.add(obstacles)

        self.speed = 0 # does not move initially
        
    def add_ice_blocks(self, *ice_blocks):
        self.ice_blocks.add(ice_blocks)
    
    def add_obstacles(self, *obstacles):
        self.obstacles.add(obstacles)

    def move(self, direction, speed):
        self.direction = pygame.math.Vector2(direction)
        self.speed = speed
        self.rect.x += self.direction.x * self.speed
        self.collision('horizontal')
        self.rect.y += self.direction.y * self.speed
        self.collision('vertical')

    def collision(self, direction):
        if direction == 'horizontal':
            for sprite in self.obstacles:   # obstacles
                if sprite.rect.colliderect(self.rect):
                    if self.direction.x > 0: # moving right
                        self.rect.right = sprite.rect.left
                    elif self.direction.x < 0: # moving left
                        self.rect.left = sprite.rect.right

            for sprite in self.ice_blocks:
                if sprite.rect.colliderect(self.rect):
                    if self.direction.x > 0: # moving right
                        self.rect.right = sprite.rect.left
                        self.direction.x, self.direction.y = 0, 0
                    elif self.direction.x < 0: # moving left
                        self.rect.left = sprite.rect.right
                        self.direction.x, self.direction.y = 0, 0 

        if direction == 'vertical':
            for sprite in self.obstacles:   # ice blocks
                if sprite.rect.colliderect(self.rect):
                    if self.direction.y > 0: # moving down
                        self.rect.bottom = sprite.rect.top
                    elif self.direction.y < 0: # moving up
                        self.rect.top = sprite.rect.bottom

            for sprite in self.ice_blocks:   # ice blocks
                if sprite.rect.colliderect(self.rect):
                    if self.direction.y > 0: # moving down
                        self.rect.bottom = sprite.rect.top
                        self.direction.x, self.direction.y = 0, 0
                    elif self.direction.y < 0: # moving up
                        self.rect.top = sprite.rect.bottom  
                        self.direction.x, self.direction.y = 0, 0 


    def update(self):
        self.move(self.direction, self.speed)


        
        
        