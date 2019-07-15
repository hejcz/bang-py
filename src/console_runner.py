import asyncio

from src.channel import TerminalChannel
from src.game import Game

asyncio.run(Game(TerminalChannel()).start())