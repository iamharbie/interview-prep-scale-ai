"""
Tests for the Finding Fish card game.
Run with: python -m unittest discover -s tests -v
"""
import unittest
import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

from finding_fish import Card, Deck, Player, RANKS, SUITS, setup_game, take_trick

RANK_VALUE = {rank: i for i, rank in enumerate(RANKS)}


def player_with(name, cards):
    p = Player(name)
    for rank, suit in cards:
        p.hand.append(Card(rank, suit))
    return p


# ─── Part 1: Deck ────────────────────────────────────────────────────────────

class TestDeck(unittest.TestCase):
    def test_deck_has_52_cards(self):
        self.assertEqual(len(Deck().cards), 52)

    def test_deck_all_unique(self):
        pairs = {(c.rank, c.suit) for c in Deck().cards}
        self.assertEqual(len(pairs), 52)

    def test_deck_covers_all_ranks_and_suits(self):
        cards = Deck().cards
        for suit in SUITS:
            for rank in RANKS:
                self.assertTrue(
                    any(c.rank == rank and c.suit == suit for c in cards),
                    f"Missing {rank} of {suit}"
                )

    def test_shuffle_changes_order(self):
        d1, d2 = Deck(), Deck()
        d2.shuffle()
        same = all(c1.rank == c2.rank and c1.suit == c2.suit for c1, c2 in zip(d1.cards, d2.cards))
        self.assertFalse(same, "Shuffled deck should not match original order")

    def test_deal_removes_top_card(self):
        deck = Deck()
        first = deck.cards[0]
        dealt = deck.deal()
        self.assertEqual(dealt.rank, first.rank)
        self.assertEqual(dealt.suit, first.suit)
        self.assertEqual(len(deck.cards), 51)

    def test_deal_empties_deck(self):
        deck = Deck()
        for _ in range(52):
            deck.deal()
        self.assertEqual(len(deck.cards), 0)


# ─── Part 1: Dealing ─────────────────────────────────────────────────────────

class TestDealing(unittest.TestCase):
    def test_four_players_returned(self):
        self.assertEqual(len(setup_game()), 4)

    def test_each_player_gets_13_cards(self):
        for p in setup_game():
            self.assertEqual(len(p.hand), 13, f"{p.name} should have 13 cards")

    def test_no_duplicate_cards_across_hands(self):
        all_cards = [(c.rank, c.suit) for p in setup_game() for c in p.hand]
        self.assertEqual(len(all_cards), len(set(all_cards)), "Duplicate cards found")

    def test_hands_sorted_by_suit_then_rank(self):
        for player in setup_game():
            suits = [c.suit for c in player.hand]
            ranks = [RANK_VALUE[c.rank] for c in player.hand]
            for i in range(1, len(player.hand)):
                if suits[i] == suits[i - 1]:
                    self.assertGreaterEqual(ranks[i], ranks[i - 1],
                        f"{player.name}'s hand not sorted by rank within suit")
                else:
                    self.assertGreaterEqual(suits[i], suits[i - 1],
                        f"{player.name}'s hand not sorted by suit")


# ─── Part 2: Playing a Card ──────────────────────────────────────────────────

class TestPlayerPlay(unittest.TestCase):
    def test_starter_plays_any_card(self):
        p = player_with("P1", [('A', 'Hearts'), ('2', 'Spades')])
        card = p.play(starter_card=None)
        self.assertIsNotNone(card)
        self.assertEqual(len(p.hand), 1)

    def test_follows_suit_when_possible(self):
        p = player_with("P1", [('2', 'Clubs'), ('K', 'Hearts')])
        card = p.play(starter_card=Card('5', 'Hearts'))
        self.assertEqual(card.suit, 'Hearts')

    def test_plays_off_suit_when_no_match(self):
        p = player_with("P1", [('2', 'Clubs'), ('K', 'Spades')])
        card = p.play(starter_card=Card('5', 'Hearts'))
        self.assertIsNotNone(card)
        self.assertEqual(len(p.hand), 1)

    def test_card_removed_from_hand_after_play(self):
        p = player_with("P1", [('A', 'Hearts')])
        p.play(starter_card=None)
        self.assertEqual(len(p.hand), 0)


# ─── Part 2: Trick Logic ─────────────────────────────────────────────────────

class TestTakeTrick(unittest.TestCase):
    def test_highest_starter_suit_wins(self):
        players = [
            player_with("P1", [('5', 'Hearts')]),
            player_with("P2", [('9', 'Hearts')]),
            player_with("P3", [('3', 'Hearts')]),
            player_with("P4", [('K', 'Hearts')]),
        ]
        self.assertEqual(take_trick(players, 0).name, "P4")

    def test_off_suit_high_card_does_not_win(self):
        players = [
            player_with("P1", [('5', 'Hearts')]),
            player_with("P2", [('A', 'Spades')]),   # off-suit ace
            player_with("P3", [('7', 'Hearts')]),
            player_with("P4", [('3', 'Diamonds')]),
        ]
        self.assertEqual(take_trick(players, 0).name, "P3")

    def test_starter_suit_is_first_players_suit(self):
        players = [
            player_with("P1", [('2', 'Clubs')]),
            player_with("P2", [('A', 'Hearts')]),
            player_with("P3", [('5', 'Clubs')]),
            player_with("P4", [('3', 'Clubs')]),
        ]
        self.assertEqual(take_trick(players, 0).name, "P3")

    def test_winner_tricks_incremented(self):
        players = [
            player_with("P1", [('A', 'Hearts')]),
            player_with("P2", [('2', 'Hearts')]),
            player_with("P3", [('3', 'Hearts')]),
            player_with("P4", [('4', 'Hearts')]),
        ]
        winner = take_trick(players, 0)
        self.assertEqual(winner.tricks, 1)

    def test_starter_idx_controls_who_leads(self):
        players = [
            player_with("P1", [('A', 'Spades')]),
            player_with("P2", [('2', 'Hearts')]),   # leads Hearts
            player_with("P3", [('K', 'Hearts')]),
            player_with("P4", [('3', 'Hearts')]),
        ]
        self.assertEqual(take_trick(players, 1).name, "P3")

    def test_cards_removed_after_trick(self):
        players = [
            player_with("P1", [('A', 'Hearts'), ('2', 'Clubs')]),
            player_with("P2", [('K', 'Hearts'), ('3', 'Clubs')]),
            player_with("P3", [('Q', 'Hearts'), ('4', 'Clubs')]),
            player_with("P4", [('J', 'Hearts'), ('5', 'Clubs')]),
        ]
        take_trick(players, 0)
        for p in players:
            self.assertEqual(len(p.hand), 1, f"{p.name} should have 1 card left")


# ─── Part 3: Full Game ───────────────────────────────────────────────────────

class TestFullGame(unittest.TestCase):
    def _run_game(self):
        players = setup_game()
        starter_idx = 0
        while any(p.hand for p in players):
            winner = take_trick(players, starter_idx)
            starter_idx = players.index(winner)
        return players

    def test_total_tricks_equals_13(self):
        players = self._run_game()
        self.assertEqual(sum(p.tricks for p in players), 13)

    def test_all_hands_empty_after_game(self):
        for p in self._run_game():
            self.assertEqual(len(p.hand), 0)


if __name__ == '__main__':
    unittest.main()
