# Polgame

Polgame is a Python library that provides an easier way to use Pygame with a different event handling mechanism. It simplifies the process of creating games and graphical applications by offering a more intuitive and flexible approach to event management.

## Features

- Simplified event handling
- Easy integration with Pygame
- Flexible and customizable

## Installation

To install Polgame, use git clone:

```bash
git clone https://github.com/POLA-LCS/polgame
```

## Getting Started

Here is a simple example to get you started with Polgame:

```python
from polgame import *

with Game('Title', 720, 480, (18, 18, 18), 60) as game:
    # Quit listener
    game.listen(pg.QUIT, lambda event: (game.close(), exit(0)))

    # Player creation
    player = game.load(Box(335, 215, 50, 50, (0, 127, 255)))
    player.radius = 25
    player_speed = 5

    # Main loop
    while game.running:
        game.listen_events()
        
        # Player movement
        if 'a' in game.active_keys:
            player.x -= player_speed
        if 'd' in game.active_keys:
            player.x += player_speed
        if 'w' in game.active_keys:
            player.y -= player_speed
        if 's' in game.active_keys:
            player.y += player_speed
            
        game.draw(player)
        game.update()
```

## Game: The main class

Game is the main class of Polgame, it has many different properties useful for game making,  
such as mouse positioning, pressed keys, framerate, entity events, etc.  
  
Arguments of class `Game` are the following:
- `title: str`  : Caption of the window.
- `width: int`  : Window's width.
- `height: int` : Window's height.
- `background_color: Color = DEFAULT_COLOR` : `DEFAULT_COLOR = (18, 18, 18)`.
- `framerate: int = 60`.  
  
The game is going to run when enter the `__enter__` method, or the context manager.

## Box: A better Rect

There's no game if there's no objects... kinda.  
`Box` is a class that inherits `pygame.Rect` and add some properties to it:  
- `color` it's the color of the Box.
- `border` it's just the border of it.

### Border

`Border` is an inner class of `Box`.  
This class has the attributes:
- `radius` : Which can be a sigle up to four values (same behaviour `border-radius` in CSS).
- `color: Color` : RGB.
- `width: int` : The width of the border in pixels.

## License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.
