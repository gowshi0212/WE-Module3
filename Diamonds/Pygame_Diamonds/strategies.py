from abc import ABC, abstractmethod
from cards import Card

from random import randint
from abc import ABC, abstractmethod
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
class LowBidStrategy(ComputerStrategy):
   def choose_bid(self, player, auction_card):
        lowest_card = min(player.cards, key=lambda card: card.value)
        return lowest_card
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