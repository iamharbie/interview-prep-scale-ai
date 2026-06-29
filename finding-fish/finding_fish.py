import random

RANKS = ['2', '3', '4', '5', '6', '7', '8', '9', '10', 'J', 'Q', 'K', 'A']
SUITS = ['Clubs', 'Diamonds', 'Hearts', 'Spades']


class Card:
    def __init__(self, rank: str, suit: str):
        self.rank = rank
        self.suit = suit

    def __repr__(self):
        return f"{self.rank} of {self.suit}"


class Deck:
    def __init__(self):
        # TODO: create self.cards — a list of all 52 Card objects
        self.cards = []

    def shuffle(self):
        # TODO: shuffle self.cards in place
        pass

    def deal(self) -> Card:
        # TODO: remove and return the top card
        pass


class Player:
    def __init__(self, name: str):
        self.name = name
        self.hand: list[Card] = []
        self.tricks = 0

    def receive(self, card: Card):
        # TODO: add card to hand
        pass

    def play(self, starter_card: Card | None = None) -> Card:
        # TODO:
        # - If starter_card is None, play any card (you are the starter)
        # - Otherwise, follow suit if possible; play any card if not
        # - Remove the chosen card from self.hand and return it
        pass

    def sort_hand(self):
        # TODO: sort hand by suit then rank (low to high)
        pass


def setup_game() -> list[Player]:
    # TODO:
    # 1. Create and shuffle a Deck
    # 2. Create 4 Players named "Player 1" .. "Player 4"
    # 3. Deal all 52 cards round-robin
    # 4. Sort and print each player's hand
    # 5. Return the list of players
    pass


def take_trick(players: list[Player], starter_idx: int = 0) -> Player:
    # TODO:
    # - Each player plays one card in order starting from starter_idx
    # - First player sets the starter suit
    # - Subsequent players must follow suit if they can
    # - Winner = player who played the highest-rank card of the starter suit
    # - Increment winner's tricks count
    # - Print each play and the winner
    # - Return the winning Player
    pass


def play_game():
    players = setup_game()
    starter_idx = 0
    trick_num = 1

    while any(p.hand for p in players):
        print(f"\n--- Trick {trick_num} ---")
        winner = take_trick(players, starter_idx)
        starter_idx = players.index(winner)
        trick_num += 1

    print("\n=== Final Scores ===")
    for player in players:
        print(f"  {player.name}: {player.tricks} trick(s)")


if __name__ == "__main__":
    play_game()
