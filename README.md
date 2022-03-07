# Ice Blocks Puzzle Game
This game is inspired by sliding block puzzles in games like The Legend of Zelda. The player must push around sliding blocks to cover each goal square to win.

## How To Play
After selecting to play a map using either the "Maps" menu or the "Play" button, you can push around sliding ice blocks on the map. To complete a map, all goals must be covered by an ice block.
### What You See On Screen
- *Player*: A blue square, slightly smaller than the other squares on screen. Controlled using the four arrow keys on keyboard. Player cannot leave the screen boundaries.
- *Ice Block*: Light blue squares that can be pushed by the player using arrow keys. An ice block moves in the direction player pushes it as long as the player is behind it. The ice block will continue to move until it collides with an obstacle such as other ice blocks, rocks, or walkable border floors.
- *Rock*: Dark gray squares that neither player nor ice blocks can move through.
- *Border Floor*: Light gray area that occurs around or in a map. The player can move on these areas, but ice blocks can not.
- *Goal*: Red squares w/ gold border line. Once all goals are covered by an ice block, a map is complete. Goals represent a clear win condition.
### Controls
- *Arrow keys*: control the player (up, down, left, right)
- *'Escape' key*: pause game, open 3-button menu ('Resume', 'Reset', 'Menus')
- *'R' key*: reset a map, every object reverts to original state and position

## Credits and Thanks
I started this project because I wanted to learn something new in software development. [PyGame](https://github.com/pygame/pygame) is a library that was fairly new to me, I wanted to create something interactive. I was able to do so thanks to tutorials online such as those from [Clear Code](https://www.youtube.com/c/ClearCode) and [Tech With Tim](https://www.youtube.com/c/TechWithTim). This game uses a font called "8-bitlimitobrk" from [Ænigma Fonts](https://www.1001fonts.com/users/kentpw/). Thank you to these creators for providing these free and public resources.
