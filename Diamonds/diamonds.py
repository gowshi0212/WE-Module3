# -*- coding: utf-8 -*-
"""Diamonds.ipynb

Automatically generated by Colab.

Original file is located at
    https://colab.research.google.com/drive/1z0zcVfi_TkvgUYLbUgJ7BtPUBzft20Ay
"""

import random

class Card:
    card_value = {2: "2", 3: "3", 4: "4", 5: "5", 6: "6", 7: "7", 8: "8", 9: "9", 10: "10", 11: "J", 12: "Q", 13: "K", 14: "A"}

    def __init__(self, suit, value):
        self.suit = suit
        self.value = value

    def get_display_name(self):
        return Card.card_value[self.value] + " of " + self.suit

class Player:
    def __init__(self, name, strategy):
        self.name = name
        self.cards = []
        self.score = 0
        if strategy:
            self.strategy = strategy(self)
        self.evaluator = CardEvaluator()
        self.observer = OpponentObserver()

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

class CardEvaluator:
    def __init__(self, remaining_diamonds=None):
        self.remaining_diamonds = remaining_diamonds  # Optional: If known

    def evaluate_card(self, card):
        value = card.value
        if self.remaining_diamonds is None:
            # General Evaluation (Without Knowing Remaining Diamonds)
            if value <= 6:
                return "Weak"  # Prioritize using weaker cards early on
            else:
                return "Strong"  # Save high-value cards for potentially valuable diamonds later
        else:
            # Consider Remaining Diamonds
            high_diamonds_remaining = sum(card.value > 6 for card in self.remaining_diamonds)
            if value <= 6 or high_diamonds_remaining <= 1:
                return "Use"  # Use the card if there are few high diamonds remaining
            else:
                return "Hold"  # Hold onto the card if there are still high diamonds to win

class OpponentObserver:

    def __init__(self):
        self.discarded_cards = []  # Track discarded cards

    def observe_discard(self, card):
        self.discarded_cards.append(card)

    def infer_hand_strength(self):
        # Analyze discarded cards to infer opponent's hand strength (basic implementation)
        high_discards = sum(card.value > 6 for card in self.discarded_cards)
        if high_discards == 0:
            return "Potentially Strong"
        elif high_discards >= 2:
            return "Likely Weak"
        else:
            return "Uncertain"

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

from abc import ABC, abstractmethod

# Define interface for pluggable computer strategies
class ComputerStrategy(ABC):
    def __init__(self, player):
        self.player = player
        self.evaluator = CardEvaluator()  # CardEvaluator instance
        self.observer = OpponentObserver()  # OpponentObserver instance

    @abstractmethod
    def choose_bid(self, auction_card):
        pass



# Example Computer Strategy (Always Bid Lowest Card)
# class LowBidStrategy(ComputerStrategy):
#     def choose_bid(self, player, auction_card):
#         lowest_card = min(player.cards, key=lambda card: card.value)
#         return lowest_card
class BoldBidding(ComputerStrategy):
    def choose_bid(self,auction_card):
        # Take risks to win valuable diamonds, potentially using high cards early
        return random.choice(self.player.cards)
class HighBidStrategy(ComputerStrategy):
    def choose_bid(self, auction_card):
        highest_card = max(self.player.cards, key=lambda card: card.value)
        return highest_card
class AlwaysExtreme(ComputerStrategy):
    def choose_bid(self, auction_card):
        # Bid the highest or lowest card based on auction card value
        if auction_card.value >= 9:  # High value - bid highest card
            return max(self.player.cards, key=lambda card: card.value)
        else:  # Low value - bid lowest card
            return min(self.player.cards, key=lambda card: card.value)
class ConservativeBidding(ComputerStrategy):
    def choose_bid(self, auction_card):
        # Prioritize low cards early on and high cards for valuable diamonds later
        remaining_cards = len(self.player.cards)
        evaluation = self.evaluator.evaluate_card(auction_card)
        if remaining_cards > (len(diamonds_cards) // 2):
            if evaluation == "Weak":
                low_card = self.get_low_card()  # Try to find a low card
                return low_card if low_card else self.get_any_card(self.player)  # Fallback: Use any card if no low card found
            else:
                # Override evaluator for low bids to avoid overpaying early
                return self.get_low_card()  # Try to find a low-ish card
        else:
            return self.get_high_card(auction_card.value)  # Prioritize high cards later

    def get_low_card(self):
        low_cards = [card for card in self.player.cards if card.value <= 6]
        return random.choice(low_cards) if low_cards else None

    def get_high_card(self, auction_card):
        # Prioritize high cards but avoid overpaying for low-value auctions
        high_cards = [card for card in self.player.cards if card.value > auction_card.value]
        return random.choice(high_cards) if high_cards else None

    def get_any_card(self):
        # Fallback method to ensure a bid is always returned
        return random.choice(self.player.cards)

class SStrategy(ConservativeBidding):
    def choose_bid(self, auction_card):
        # Consider remaining cards, opponent observations, and game stage
        remaining_cards = len(self.player.cards)
        opponent_strength = self.observer.infer_hand_strength()
        evaluation = self.evaluator.evaluate_card(auction_card)

        # Early Game (More Cards Remaining)
        if remaining_cards > (len(diamonds_cards) // 2):
            if opponent_strength == "Likely Weak":
                # Exploit weakness with mid-tier cards
                return random.choice([card for card in self.player.cards if 4 <= card.value <= 7])
            else:
                # Play it safe or compete for valuable diamonds (use parent logic)
                return super().choose_bid(auction_card)

        # Late Game (Fewer Cards Remaining)
        else:
            if opponent_strength == "Potentially Strong":
                # Focus on using strong cards to potentially win valuable diamonds
                return self.get_high_card(auction_card.value)  # Override parent logic
            else:
                # Use parent logic for adapting bids based on card evaluation
                return super().choose_bid(auction_card)

# Game Logic
def play_diamonds_game(num_players):
    num_cards_per_player = 13

    # Distribute remaining cards (Hearts, Clubs, Spades) based on number of players
    player_cards = []
    if num_players == 2:
        player_cards.append(hearts_cards)
        player_cards.append(clubs_cards)


    elif num_players == 3:
        player_cards.append(hearts_cards)  # Split hearts for 3 players
        player_cards.append(clubs_cards)  # Split clubs for 3 players
        player_cards.append(spades_cards)  # Split spades for 3 players
    else:
        raise NotImplementedError("Currently only supports 2 or 3 players")

    # Create players and assign cards
    players = []
    for i in range(num_players):
        if i == 0:
            # User is always player 1
            players.append(UserPlayer(f"Player {i+1}", None))
        else:
            # Assign a computer strategy (example: LowBidStrategy)
            players.append(ComputerPlayer(f"Computer {i+1}", random.choice([
    BoldBidding ,  # Provide placeholder player for now
    HighBidStrategy ,  # Assuming this is also a ComputerStrategy subclass
    ConservativeBidding ,
    AlwaysExtreme,
    SStrategy
])))

            # players.append(ComputerPlayer(f"Computer {i+1}", random.choice([BoldBidding(),HighBidStrategy(),ConservativeBidding(),AlwaysExtreme()])))
        players[i].receive_cards(player_cards[i])

    # Main game loop
    for _ in range(num_cards_per_player):  # Play until all cards are used
        # Draw auction card
        print("_________________________________________________")
        auction_card = diamonds_cards.pop()

        # Bidding round
        highest_bid = None
        highest_bidders = []  # List to store players with the highest bid
        for player in players:
            bid = player.choose_bid(auction_card)
            if highest_bid is None or bid.value > highest_bid.value:
                highest_bid = bid
                highest_bidders = [player]  # Clear the list and add the new leader
            elif highest_bid is not None and bid.value == highest_bid.value:
                highest_bidders.append(player)  # Add another player to the tie list

        # Award points to winners (split if tie)
        if len(highest_bidders) == 1:
            for winner in highest_bidders:
                points_per_winner = auction_card.value
                winner.add_points(points_per_winner)
                print(f"{winner.name} wins with {highest_bid.get_display_name()} ({points_per_winner} points)")
        elif highest_bidders:
            points_per_winner = auction_card.value / len(highest_bidders)
            for winner in highest_bidders:
                winner.add_points(points_per_winner)
                print(f"{winner.name} wins with {highest_bid.get_display_name()} (tie, {points_per_winner} points each)")

        # Print game state (optional)
        print(f"Auction Card: {auction_card.get_display_name()}")
        for player in players:
            print(f"{player.name} Score: {player.score}")

    # Check for tie in final scores
    highest_score = max(player.score for player in players)
    tied_players = [player for player in players if player.score == highest_score]
    if len(tied_players) > 1:
        # Announce tie if multiple players have the highest score
        player_names = ", ".join(player.name for player in tied_players)
        print(f"It's a tie! {player_names} all have the highest score of {highest_score} points.")
    else:
        # Announce winner if there's no tie
        winner = max(players, key=lambda player: player.score)
        print(f"Winner: {winner.name}")

# Create separate lists for each suit
hearts_cards = []
clubs_cards = []
spades_cards = []
diamonds_cards = []

for value in range(2, 15):
    hearts_cards.append(Card("Hearts", value))
    clubs_cards.append(Card("Clubs", value))
    spades_cards.append(Card("Spades", value))
    diamonds_cards.append(Card("Diamonds", value))

# Shuffle Diamonds only
random.shuffle(diamonds_cards)

# Play the game with a chosen number of players
num_players = int(input("Enter the number of players (2 or 3): "))
if num_players not in [2, 3]:
    print("Invalid number of players. Please enter 2 or 3.")
else:
    play_diamonds_game(num_players)