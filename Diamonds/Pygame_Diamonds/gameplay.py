import random
from strategies import *
from cards import Card, Deck
from ui import UI


class Player:
    def __init__(self, name, strategy):
        self.name = name
        self.cards = []
        self.score = 0
        if strategy:
            self.strategy = strategy(self)
        self.evaluator = CardEvaluator()
        self.observer = OpponentObserver()
    
    def SetStrategy(self, strategy):
       self.strategy = strategy

    def receive_cards(self, cards):
        self.cards.extend(cards)

    def choose_bid(self, auction_card):
        if self.strategy == None:  # User player
            return self.get_user_bid(auction_card)
        return self.strategy.choose_bid(self, auction_card)

    def get_user_bid(self, auction_card):
        print(f"Auction Card: {auction_card.get_display_name()}")
        print(f"Your Hand:")
        for i, card in enumerate(self.cards):
            print(f"{i+1}. {card.get_display_name()}")

        while True:
            try:
                bid_index = int(input(f"Enter the index of the card you want to bid (1-{len(self.cards)}): ")) - 1
                if 0 <= bid_index < len(self.cards):
                    return self.cards.pop(bid_index)  # Remove and return card
                else:
                    print("Invalid index. Please enter a number between 1 and", len(self.cards))
            except ValueError:
                print("Invalid input. Please enter a number.")

    def add_points(self, points):
        self.score += points

    def discard_card(self, card_index):
        if 0 <= card_index < len(self.cards):
            self.cards.pop(card_index)  # Remove card by index
        else:
            print(f"Invalid card index: {card_index}. Card not discarded.")



class ComputerPlayer(Player):

    def choose_bid(self, auction_card):
        chosen_card = self.get_computer_bid(auction_card)
        self.discard_card(self.cards.index(chosen_card))  # Remove card by index
        return chosen_card

    def get_computer_bid(self, auction_card):
        chosen_card = self.strategy.choose_bid(auction_card)
        print(f"{self.name} bids with {chosen_card.get_display_name()}")
        return chosen_card


class UserPlayer(Player):
    def choose_bid(self, auction_card):
        chosen_card = self.get_user_bid(auction_card)
        return chosen_card
class DiamondsGame:
  """
  Class to manage the overall gameplay logic and interact with the UI.
  """
  def __init__(self, num_players=2, ui=None):
    self.num_players = num_players
    self.players = []
    self.bidding_cards = Deck(suit = "Diamonds")
    self.hearts_cards = Deck(suit="Hearts")
    self.clubs_cards = Deck(suit="Clubs")
    self.spades_cards = Deck(suit="Spades")
    self.ui = UI  # Reference to UI object (optional)
    self.game_state = "setup"  # Initial game state

  def setup_game(self):
    # Shuffle Diamonds deck
    random.shuffle(self.bidding_cards)

    # Create players (one UserPlayer and others ComputerPlayer)
    for i in range(self.num_players):

      if i == 0:
        self.players.append(UserPlayer(f"Player {i+1}", None))
        continue #I dont understand why this continue is necessary, but it works only with it
      else:
        self.players.append(ComputerPlayer(f"Computer {i+1}", None))
        strategy = random.choice([ConservativeBidding(self.players[i]), BoldBidding(self.players[i])])
        self.players[i].SetStrategy(strategy)
  

      # Deal cards (except Diamonds)
      num_cards_per_player = 13
      carddecks = (self.hearts_cards, self.spades_cards, self.clubs_cards)
 
      for i in range(self.num_players):
        self.players[i].receive_cards(carddecks[i])

    # Remove dealt cards from remaining deck
    #self.remaining_cards.remove(self.hearts_cards.cards + self.clubs_cards.cards + self.spades_cards.cards)

    self.game_state = "in_game"  # Update game state

  def play_game(self):
    # Main game loop
    while self.game_state == "in_game":
      # Draw auction card
      auction_card = self.diamonds_cards.draw(1)[0]
      self.ui.display_auction_card()
      # Bidding round
      highest_bid = None
      highest_bidders = []
      for player in self.players:
        chosen_card = player.choose_bid(auction_card, self.ui)  # Get chosen card using UI

        # Update UI with chosen card (if UI available)
        if self.ui:
          self.ui.display_chosen_card(player, chosen_card)

        if highest_bid is None or chosen_card.value > highest_bid.value:
          highest_bid = chosen_card
          highest_bidders = [player]
        elif highest_bid is not None and chosen_card.value == highest_bid.value:
          highest_bidders.append(player)

      # Award points to winners (split if tie)
      self.award_points(highest_bidders, auction_card)

      # Update UI with game state (if UI available)
      if self.ui:
        self.ui.update_game_state(auction_card, self.players)

      # Check for game end
      if len(self.diamonds_cards) == 0:
        self.game_state = "game_over"

    # Declare winner (call UI method)
    winner = self.get_winner()
    if self.ui:
      self.ui.declare_winner(winner)

  def award_points(self, winners, auction_card):
    points_per_winner = auction_card.value
    for winner in winners:
      winner.add_points(points_per_winner)

  def get_winner(self):
    highest_score = max(player.score for player in self.players)
    tied_players = [player for player in self.players if player.score == highest_score]
    if len(tied_players) > 1:
      return None  # Tie
    else:
      return tied_players[0]



