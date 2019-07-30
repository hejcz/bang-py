import asyncio
from random import shuffle

from src.channel import TerminalChannel
from src.game import Game

cards = [
    ["bang"] * 25,
    ["stagecoach"] * 2,
    ["indians"] * 2,
    ["shop"] * 2,
    ["kate"] * 4,
    ["duel"] * 3,
    ["beer"] * 6,
    ["panic"] * 4,
    ["dodge"] * 11,
    ["saloon", "gatling", "wells_fargo"]
]

deck = [item for sublist in cards for item in sublist]
shuffle(deck)

asyncio.run(Game(TerminalChannel(), ["tom", "julian"], deck).start())