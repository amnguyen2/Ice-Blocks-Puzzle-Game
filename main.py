import pygame, sys
from level import Level
from map import read_maps
from settings import * 
"""
Notes:
    - Must separate 'View' and 'Control' aspects of this program. 'Model' aspect is complete and separate.
    - Some functionality should be implemented in the future, including
        - easy and intuitive map creation
        - allow user to play maps continuously after completion w/out returning to menus
        - map hints
        - more game objects to add complexity to maps (pitfalls, lava, portals, ...)
"""

"""
User can pause a map and select to:
    - Resume: remove the Pause Menu and continue game loop
    - Reset: remove the Pause Menu and start the game loop again (place every game object in its starting place)
    - Menus: remove the Pause Menu and leave the game loop to enter the Main Menu
"""
def pause_menu(clock, screen):
    # create menu buttons
    button_x = screen.get_width()/2 - BUTTON_W/2
    button_y = screen.get_height()/2 - BUTTON_H/2*3
    button_pos1 = (button_x, button_y)
    button_pos2 = (button_x, button_y+BUTTON_H+BUTTON_SPACE)
    button_pos3 = (button_x, button_y+(BUTTON_H*2)+(BUTTON_SPACE*2))

    resume_button = draw_button(screen, "Resume", button_pos1, (BUTTON_W, BUTTON_H), BUTTON_COLOR, TEXT_COLOR)
    reset_button = draw_button(screen, "Reset", button_pos2, (BUTTON_W, BUTTON_H), BUTTON_COLOR, TEXT_COLOR)
    menu_button = draw_button(screen, "Menus", button_pos3, (BUTTON_W, BUTTON_H), BUTTON_COLOR, TEXT_COLOR)

    # pause menu logic
    command = 'pause'
    while command == 'pause':
        # input handling
        for event in pygame.event.get():    # check for any user actions
            if event.type == pygame.QUIT:
                pygame.quit()               # uninitialize pygame module
                sys.exit()                  # close program
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    command = 'resume'
            elif event.type == pygame.MOUSEBUTTONUP:   # check button click
                mx, my = pygame.mouse.get_pos()
                if resume_button.collidepoint((mx, my)):  # click 'Resume'
                    command = 'resume'
                elif reset_button.collidepoint((mx, my)):    # click 'Reset'
                    command = 'reset'
                elif menu_button.collidepoint((mx, my)):    # click 'Quit'
                    command = 'menu'

        pygame.display.flip()               # update full display surface to screen
        clock.tick(24)                      # 24 fps

    return command

"""
When a map's win condition has been met, game loop is stopped. Give the user options to:
    - Replay: remove the Win Menu and start the game loop again (place every game object in its starting place)
    - Menus: remove the Win Menu and enter the Main Menu
"""
def win_menu(clock, screen):
    button_x = screen.get_width()/2 - BUTTON_W/2
    button_y = screen.get_height()/2 - BUTTON_H/2*3
    msg_pos1 = (0, button_y/2)
    button_pos2 = (button_x, button_y+BUTTON_H+BUTTON_SPACE)
    button_pos3 = (button_x, button_y+(BUTTON_H*2)+(BUTTON_SPACE*2))

    # draw 'map complete'
    map_complete_msg = draw_button(screen, "Map Complete", msg_pos1, (screen.get_width(), BUTTON_H), WIN_RECT_COLOR, TEXT_COLOR)
    reset_button = draw_button(screen, "Replay", button_pos2, (BUTTON_W, BUTTON_H), BUTTON_COLOR, TEXT_COLOR)
    menu_button = draw_button(screen, "Menus", button_pos3, (BUTTON_W, BUTTON_H), BUTTON_COLOR, TEXT_COLOR)

    # pause menu logic
    command = 'pause'
    while command == 'pause':
        # input handling
        for event in pygame.event.get():    # check for any user actions
            if event.type == pygame.QUIT:
                pygame.quit()               # uninitialize pygame module
                sys.exit()                  # close program
            elif event.type == pygame.MOUSEBUTTONUP:   # check button click
                mx, my = pygame.mouse.get_pos()
                if reset_button.collidepoint((mx, my)):    # click 'Reset'
                    command = 'reset'
                elif menu_button.collidepoint((mx, my)):    # click 'Quit'
                    command = 'menu'

        pygame.display.flip()               # update full display surface to screen
        clock.tick(24)                      # 24 fps

    return command

"""
Game loop. 'play_game' function has control over the game and outlines its logic.
See 'gameObject.py' comments for details in game functionality.
"""
def play_game(clock, game_map):
    # setting up main window
    screen_w = game_map.size[0] * BLOCK_SIZE
    screen_h = game_map.size[1] * BLOCK_SIZE
    screen = pygame.display.set_mode((screen_w, screen_h))  # display surface (only 1 instance)
    pygame.display.set_caption(TITLE)                       # window title

    level = Level()
    level.setup(game_map)
    command = 'play'
    
    has_won = False
    while not has_won and ((command != 'menu') and (command != 'reset')):

        # input handling
        for event in pygame.event.get():    # check for any user actions
            if event.type == pygame.QUIT:
                pygame.quit()               # uninitialize pygame module
                sys.exit()                  # close program
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    command = pause_menu(clock, screen)
                if event.key == pygame.K_r:
                    command = 'reset'

        screen.fill(FLOOR_COLOR)            # draw background

        level.stiff_sprites.draw(screen)          # draw sprites/objects to screen
        level.goal_sprites.draw(screen)
        level.player_sprite.draw(screen)   
        level.ice_sprites.draw(screen)      
        
        level.player_sprite.update()              # update sprites' pos, direction
        level.ice_sprites.update()          
    
        pygame.display.flip()               # update full display surface to screen
        clock.tick(60)                      # 60 fps

        # check win condition (all goals pos == any ice pos))
        has_won = level.check_win()
        if has_won:
            level.stiff_sprites.draw(screen)          # draw sprites' last frame
            level.goal_sprites.draw(screen)
            level.player_sprite.draw(screen)   
            level.ice_sprites.draw(screen)      
    
            command = win_menu(clock, screen)

    return command

"""
Custom draw method that takes parameters required 
to draw custom buttons or messages on screen.
"""
def draw_button(screen, name, pos, size, b_color, txt_color):
    button = pygame.Rect(pos[0], pos[1], size[0], size[1])
    text = pygame.font.Font(UI_FONT, UI_FONT_SIZE)
    button_text = text.render(name, True, txt_color)
    pygame.draw.rect(screen, (b_color), button)
    textRect = button_text.get_rect()
    textRect.center = button.center
    screen.blit(button_text, textRect)

    return button

"""
Displays a grid of all available maps on screen 
as buttons for user to select from. 
* Note: Cannot yet create more than one row of map buttons.
"""
def map_select(clock):
    # setting up screen
    screen_w = MENU_SCREEN_W
    screen_h = MENU_SCREEN_H
    screen = pygame.display.set_mode((screen_w, screen_h))  # display surface (only 1 instance)
    pygame.display.set_caption(TITLE)                       # window title
    screen.fill((FLOOR_COLOR))

    map_list = read_maps()  # list of maps from map file
    loaded_map = map_list[0]
    map_buttons = []        # list of buttons for maps
    BUTTON_SPACE = 10       # space between buttons on screen
    for num in range(len(map_list)):    # create button for each map
        curr_map = map_list[num]
        button_pos = ((BUTTON_W*num) + (BUTTON_SPACE*(num+1)), BUTTON_SPACE)  # calculate button position
        button = draw_button(screen, curr_map.name, button_pos, (BUTTON_W, BUTTON_H), BUTTON_COLOR, TEXT_COLOR)   # draw map grid squares
        map_buttons.append(button)
        
    # input handling (click buttons to select a map to load)
    command = 'maps'
    while command == 'maps':
        # input handling
        for event in pygame.event.get():    # check for any user actions
            if event.type == pygame.QUIT:
                pygame.quit()               # uninitialize pygame module
                sys.exit()                  # close program
            # check which map button was clicked
            if event.type == pygame.MOUSEBUTTONUP:   # check button click
                mx, my = pygame.mouse.get_pos()
                for num in range(len(map_buttons)):
                    if map_buttons[num].collidepoint((mx, my)):  # click 'Play'
                        return map_list[num]

        pygame.display.flip()               # update full display surface to screen
        clock.tick(24)                      # 24 fps

    return loaded_map

"""
The Main Menu is where the user 'enters' the program. 
Give the user options to:
    - Play: start game loop
    - Maps: view grid of available maps on screen
    - Quit: close the program
"""
def main_menu(clock):
    # setting up screen
    screen_w = MENU_SCREEN_W
    screen_h = MENU_SCREEN_H
    screen = pygame.display.set_mode((screen_w, screen_h))  # display surface (only 1 instance)
    pygame.display.set_caption(TITLE)                       # window title

    # draw main menu 
    screen.fill((FLOOR_COLOR))
    play_pos = (MENU_BUTTON_X, MENU_BUTTON_Y)
    maps_pos = (MENU_BUTTON_X, MENU_BUTTON_Y+BUTTON_H+BUTTON_SPACE)
    quit_pos = (MENU_BUTTON_X, MENU_BUTTON_Y+(BUTTON_H*2)+(BUTTON_SPACE*2))

    play_button = draw_button(screen, "play", play_pos, (BUTTON_W, BUTTON_H), BUTTON_COLOR, TEXT_COLOR)
    maps_button = draw_button(screen, "maps", maps_pos, (BUTTON_W, BUTTON_H), BUTTON_COLOR, TEXT_COLOR)
    quit_button = draw_button(screen, "quit", quit_pos, (BUTTON_W, BUTTON_H), BUTTON_COLOR, TEXT_COLOR)
    
    # main menu logic
    command = 'menu'
    while command == 'menu':
        # input handling
        for event in pygame.event.get():    # check for any user actions
            if event.type == pygame.QUIT:
                pygame.quit()               # uninitialize pygame module
                sys.exit()                  # close program
            if event.type == pygame.MOUSEBUTTONUP:   # check button click
                mx, my = pygame.mouse.get_pos()
                if play_button.collidepoint((mx, my)):  # click 'Play'
                    command = 'play'
                elif maps_button.collidepoint((mx, my)):    # click 'Maps'
                    command = 'maps'
                elif quit_button.collidepoint((mx, my)):    # click 'Quit'
                    command = 'quit'

        pygame.display.flip()               # update full display surface to screen
        clock.tick(24)                      # 24 fps

    return command

"""
Main logic loop. Handles 'commands' that are returned by 
each 'Control' function to decide what the program must do next.
"""
def main():
    # general setup
    pygame.init()                       # initiates pygame modules
    clock = pygame.time.Clock()         

    map_list = read_maps()              # initialize maps
    loaded_map = map_list[0]
    
    command = main_menu(clock)
    while True:
        if command == 'play':
            command = play_game(clock, loaded_map)
        elif command == 'maps':
            loaded_map = map_select(clock)
            command = play_game(clock, loaded_map)
        elif command == 'reset':
            command = play_game(clock, loaded_map)
        elif command == 'menu':
            command = main_menu(clock)
        elif command == 'quit':
            pygame.quit()               # uninitialize pygame module
            sys.exit()                  # close program
        else:
            print('ERROR: Command not found: \"', command, "\"")
            pygame.quit() 
            sys.exit()             

if __name__ == "__main__":
    main()