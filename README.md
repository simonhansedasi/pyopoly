# pyopoly

### A game for slumlords.

Terminal-based Monopoly clone with CPU opponents, colorized output, and the full mechanics: properties, rent, auctions, jail, and card decks.

## What it does

Implements Monopoly in Python with human vs. AI players. Features property ownership, building houses/hotels, custom card decks (Chance/Community Chest), jail mechanics, and a color-coded terminal UI.

- **CPU AI** — automated buy, build, mortgage, and trade decisions
- **Trading** — humans can propose trades with any player; CPUs proactively seek trades to complete monopolies (CPU-to-CPU and CPU-to-human)
- **Auctions** — properties declined by the landing player go to open auction
- **Jail** — pay bail, roll for doubles, or burn a Get Out of Jail Free card
- **Mortgaging** — mortgage/unmortgage properties from the in-turn menu

## Tech

Python — stdlib only (`random`, `time`, ANSI color codes)

## Run

```bash
python pyopoly.py
```
