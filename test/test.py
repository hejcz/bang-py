import unittest

from src.channel import Channel
from src.commands import BangCommand
from src.game import Game
from src.notifications import Info


class TestChannel(Channel):

    def __init__(self) -> None:
        super().__init__()


class TestSum(unittest.TestCase):

    def test_no_error_on_bang_skip(self):
        running_game = Game(TestChannel()).game_runner()
        step = running_game.send(None)
        self.assertTrue(isinstance(step["content"], Info), "should be info")
        self.assertEqual(step["content"].msg, Info.PLAY_CARD, "should be play card")
        step = running_game.send(BangCommand("tom"))
        print(step["content"].player)


if __name__ == '__main__':
    unittest.main()
