import unittest

from game import Game


class TestSum(unittest.TestCase):

    def test_no_error_on_bang_skip(self):
        running_game = Game(None).game_runner()
        step = running_game.send(None)
        self.assertEqual(step["content"]['type'], "info", "should be info")
        self.assertEqual(step["content"]['msg'], "play card!", "should be play card")
        step = running_game.send({"hello": "world"})
        print(step)


if __name__ == '__main__':
    unittest.main()
