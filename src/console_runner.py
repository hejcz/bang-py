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
    ["saloon", "gatling", "wells_fargo"],
    # TODO
    ["prison"] * 3,
    ["barell"] * 2,
    ["horse"] * 2,
    ["shofield"] * 3,
    ["volcanic"] * 2,
    ["dynamite", "winchester", "remington", "rev_carabine", "field_glass"]
]

deck = [item for sublist in cards for item in sublist]
shuffle(deck)

asyncio.run(Game(TerminalChannel(), ["tom", "julian"], deck).start())
