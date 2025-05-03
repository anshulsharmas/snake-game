# Snake Game

A classic Snake game in Python built using Cursor, featuring power-ups and background music.


## Features
- Classic snake gameplay
- Score tracking
- Adjustable game speed
- Responsive controls
- Modern visual design
- Power-up system
- Background music and sound effects

## Power-ups
The game features various power-ups that spawn randomly (20% chance when collecting food):

- ⚡ Speed Boost: Temporarily increases snake's speed (10 seconds)
- 🛡️ Shield: Makes the snake's first body segment yellow, indicating protection (8 seconds)
- 2x Double Points: Gives bonus points when collecting food (12 seconds)
- 👻 Ghost: Allows the snake to pass through its own body (8 seconds)

## Requirements
- Python 3.x
- Pygame
- NumPy

## Installation
1. Clone the repository
2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

## How to Play
1. Run the game:
   ```bash
   python snake_game.py
   ```
2. Use arrow keys to control the snake
3. Press +/- to adjust game speed
4. Press F to toggle fullscreen
5. Press M to toggle background music
6. Press SPACE to restart after game over

## Controls
- ↑ Up Arrow: Move up
- ↓ Down Arrow: Move down
- ← Left Arrow: Move left
- → Right Arrow: Move right
- +: Increase speed (max: 10)
- -: Decrease speed (min: 1)
- F: Toggle fullscreen
- M: Toggle background music
- SPACE: Restart game

## Sound Effects
The game includes various sound effects:
- Soothing background music (toggle with M key)
- Food collection sound
- Power-up collection sound
- Game over sound

![Game Screenshot](/img/game.png)
