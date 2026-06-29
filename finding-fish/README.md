# Finding Fish — Scale AI Interview Practice

A Python implementation exercise for the "Finding Fish" card game, based on a real Scale AI coding interview.

## Structure

```
finding-fish/
├── finding_fish.py       ← fill in the TODOs
└── tests/
    └── test_finding_fish.py
```

## The Problem

Implement a trick-taking card game for 4 players using a standard 52-card deck.

### Part 1 — Setup & Dealing
- Build a 52-card deck and shuffle it
- Deal cards round-robin to 4 players (13 each)
- Print each player's hand in sorted order (by suit, then rank low→high)

### Part 2 — Playing a Trick
- Each player plays one card per trick
- The first player may play any card — their suit becomes the **starter suit**
- Subsequent players must follow suit if they can; otherwise play any card
- The player who played the **highest-rank card of the starter suit** wins
- Return the winning player

### Part 3 — Scoring
- Track tricks won per player
- Print final scores after all 13 tricks are played

## Running the Tests

No dependencies needed — uses Python's built-in `unittest`:

```bash
cd finding-fish
python -m unittest discover -s tests -v
```

## Running the Game

```bash
python finding_fish.py
```
