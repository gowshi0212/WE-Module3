# ui.py

import pygame
from pygame.locals import *
from cards import Card
import os

pygame.init()

class UI:
  """
  Class to handle the Pygame UI elements and interact with the game.
  """
  WHITE = (255, 255, 255)
  GREEN = (0, 255, 0)
  DARKGREEN = (1, 50, 32)
  BLACK = (0, 0, 0)
  CARD_WIDTH = 60.5
  CARD_HEIGHT = 85
  BUTTON_WIDTH = 150
  BUTTON_HEIGHT = 50
  FONT = pygame.font.SysFont(None, 32)

  def __init__(self, screen_width, screen_height):
    pygame.init()
    self.flags = pygame.RESIZABLE
    self.screen = pygame.display.set_mode((screen_width, screen_height), self.flags)
    self.screen.fill("pink")
    self.card_images = self.load_card_images()
    self.card_back_image = pygame.image.load("playing-cards-master/back_dark.png").convert_alpha()
    self.game = None  # Reference to DiamondsGame object (set later)
    self.current_scene = "setup"  # Initial scene
    self.show_computer_cards = False
  def load_card_images(self):
    images = {}
    images_smaller = {}
    for suit in ["Clubs", "Diamonds", "Hearts", "Spades"]:
      for value in range(2, 15):
        print(suit, value)
        card_value = {2: "2", 3: "3", 4: "4", 5: "5", 6: "6", 7: "7", 8: "8", 9: "9", 10: "10", 11: "J", 12: "Q", 13: "K", 14: "A"}
        filename = f"playing-cards-master/{suit}_{card_value[value]}.png"
        images[(suit, value)] = pygame.image.load(filename).convert_alpha()
        images_smaller[(suit, value)] = pygame.transform.scale(images[(suit, value)], (60.5, 85))
    return images_smaller

  def display_card(self, card, x, y):
    if card is None:
      self.screen.blit(self.card_back_image, (x, y))
    else:
      print(self.card_images)
      self.screen.blit(self.card_images[(card.suit, card.value)], (x, y))

  def display_button(self, text, x, y, width, height, color, hover_color, click_func):
    # Draw button background and text
    button_rect = pygame.Rect(x, y, width, height)
    mouse_x, mouse_y = pygame.mouse.get_pos() 
    self.screen.fill(hover_color if mouse_x in range(button_rect.left, button_rect.right + 1) and 
                 mouse_y in range(button_rect.top, button_rect.bottom + 1) else color, button_rect)
    text_surface = self.FONT.render(text, True, self.BLACK)
    text_x = button_rect.centerx - text_surface.get_width() // 2
    text_y = button_rect.centery - text_surface.get_height() // 2
    self.screen.blit(text_surface, (text_x, text_y))

    # Check for button click
    if pygame.mouse.get_pressed()[0] and button_rect.collidepoint(pygame.mouse.get_pos()):
      click_func()

  def display_hand(self, hand, player_position = 20):
    # Clear screen and set background color
    self.screen.fill(self.DARKGREEN)

    # Display each card in the hand with some spacing
    for i, card in enumerate(hand):
      self.display_card(card, i * (self.CARD_WIDTH + 1), player_position)
    for i, card in enumerate(hand):
      if not self.game.is_current_player(i) and not self.show_computer_cards:
        self.screen.blit(self.card_back_image, (x, y))
      else:
        self.screen.blit(self.card_images[(card.suit, card.value)], (x, y))
    # Update the display
    pygame.display.flip()

  def display_auction_card(self, card):
    # Draw auction card at a specific location
    self.display_card(card, self.screen.get_width() // 2 - self.CARD_WIDTH // 2, self.screen.get_height() // 2 - self.CARD_HEIGHT // 2)

    # Display text for Auction Card
    auction_text = self.FONT.render("Auction Card", True, self.BLACK)
    self.screen.blit(auction_text, (self.screen.get_width() // 2 - auction_text.get_width() // 2, self.screen.get_height()// 2))

    # Update the display
    pygame.display.flip()

  def display_chosen_card(self, player, chosen_card):
    """
    Highlights the chosen card's image in the player's hand.

    Args:
        player: The Player object representing the current player.
        chosen_card: The Card object that the player has chosen.
    """
    card_rect = card_image.get_rect()  # Base rectangle for card image
    alpha_surface = pygame.Surface(card_rect.size, pygame.SRCALPHA)  # Create alpha surface
    alpha_surface.fill((255, 255, 255, 128))  # Set partial transparency

    for i, card in enumerate(player.cards):
      # Highlight chosen card's image with alpha surface
      if card == chosen_card:
        card_rect.x = 50 + (i * card_rect.width)
        card_rect.y = screen_height // 2
        screen.blit(card_image, card_rect)
        screen.blit(alpha_surface, card_rect)  # Overlay alpha surface for highlight

      card_rect.x = 50 + (i * card_rect.width)
      card_rect.y = screen_height // 2
      screen.blit(card_image, card_rect)
      card_text = font.render(card.get_display_name(), True, BLACK)
      text_rect = card_text.get_rect(center=card_rect.center)
      screen.blit(card_text, text_rect)

  def display_game_state(self, auction_card, players):
    # Clear screen and set background color
    self.screen.fill(self.WHITE)

    # Display auction card again
    self.display_auction_card(auction_card)

    # Display player names and scores
    for i, player in enumerate(players):
      player_text = self.FONT.render(f"{player.name}: {player.score}", True, self.BLACK)
      self.screen.blit(player_text, (10, self.screen.get_height() // 2 + 50 * i))

    # Update the display
    pygame.display.flip()

  def handle_setup_scene(self):
    # Display "Start Game" button
    self.display_button("Start Game", self.screen.get_width() // 2 - self.BUTTON_WIDTH // 2, self.screen.get_height() // 2, self.BUTTON_WIDTH, self.BUTTON_HEIGHT, self.GREEN, self.DARKGREEN, self.start_game)

  def handle_in_game_scene(self, current_player):
    self.screen.fill("purple")
    # Display player's hand
    self.display_hand(current_player.cards)

    # Display buttons for each card in hand (optional for user bidding)
    for i, card in enumerate(current_player.cards):
      x = i * (self.CARD_WIDTH + 20) + 10  # Adjust positioning
      y = self.screen.get_height() - self.CARD_HEIGHT - 20  # Adjust positioning
      # Implement button logic to choose card (pass card index to game)

  def handle_game_over_scene(self, winner):
    # Display winner information
    winner_text = self.FONT.render(f"{winner.name} Wins!", True, self.GREEN)
    self.screen.blit(winner_text, (self.screen.get_width() // 2 - winner_text.get_width() // 2, self.screen.get_height() // 2))

    # Display "Play Again" button (optional)

  def start_game(self):
    # Set reference to DiamondsGame object and update scene
    self.game.setup_game()
    self.current_scene = "in_game"

  def run_game(self, game):
    self.game = game
    clock = pygame.time.Clock()
    running = True
    while running:
      for event in pygame.event.get():
        if event.type == pygame.QUIT:
          running = False

      # Handle events based on current scene
      if self.current_scene == "setup":
        self.screen.fill("pink")
        self.handle_setup_scene()
      elif self.current_scene == "in_game":
        self.screen.fill("self.DARKGREEN")
        current_player = self.game.players[0]  # Assuming user is player 1
        self.handle_in_game_scene(current_player)
        # Implement logic to get user card choice and pass to game
        # Update scene based on game state (e.g., after bidding round)
      elif self.current_scene == "game_over":
        self.screen.fill("pink")
        winner = self.game.get_winner()
        self.handle_game_over_scene(winner)

      # Update the display
      pygame.display.flip()
      clock.tick(60)  # Limit to 60 FPS

    pygame.quit()

# Example Usage (


