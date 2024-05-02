import random
card_value = {2: "2", 3: "3", 4: "4", 5: "5", 6: "6", 7: "7", 8: "8", 9: "9", 10: "10", 11: "J", 12: "Q", 13: "K", 14: "A"}
class Card:
  """
  Represents a playing card with suit and value.
  """

  def __init__(self, suit, value):
    if suit not in ["Hearts", "Diamonds", "Clubs", "Spades"]:
      raise ValueError(f"Invalid suit: {suit}")
    if value not in list(card_value.keys()):
      raise ValueError(f"Invalid value: {value}")
    self.suit = suit
    self.value = value

  def get_display_name(self):
    """
    Returns the display name of the card (e.g., "2 of Hearts").
    """
    return card_value[self.value] + " of " + self.suit
  
#   def __eq__(Card2):
#     return self.suit == Card2.suit and self.value == Card2.value

def Deck(suit):
  
    if suit not in ["Hearts", "Diamonds", "Clubs", "Spades"]:
      raise ValueError(f"Invalid suit: {suit}")
    return[Card(suit, value) for value in card_value.keys()]