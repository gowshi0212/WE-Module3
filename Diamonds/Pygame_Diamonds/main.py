import pygame
from gameplay import DiamondsGame
from ui import UI

# Initialize Pygame
pygame.init()

# Set screen dimensions
screen_width = 1000
screen_height = 1000

# Create DiamondsGame object
game = DiamondsGame()

# Create UI object and link it with the game
ui = UI(screen_width, screen_height)
ui.game = game

# Run the game loop using the UI
ui.run_game(game)

# Quit Pygame when finished
pygame.quit()
