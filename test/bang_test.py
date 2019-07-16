import unittest

from src.channel import Channel
from src.commands import BangCommand, SkipCommand
from src.game import Game
from src.notifications import Error


class TestChannel(Channel):

    def __init__(self) -> None:
        super().__init__()


class TestSum(unittest.TestCase):

    @staticmethod
    def prepare_game():
        game = Game(TestChannel())
        running_game = game.game_runner()
        running_game.send(None)
        return game, running_game

    def test_player_cant_bang_himself(self):
        (game, running_game) = self.prepare_game()
        self.assertEqual(game.state.current_player.health, 4, "should be equal to initial value")
        running_game.send(BangCommand("tom"))
        step = running_game.send(SkipCommand())
        self.assertIsInstance(step["content"], Error, "error should be detected")

    def test_must_drop_enough_cards(self):
        """
        If player has 4 health and 6 cards then he must drop at least 2 cards.
        """
        (game, running_game) = self.prepare_game()
        pass

    def test_cant_play_card_that_he_has_not_in_hand(self):
        (game, running_game) = self.prepare_game()
        pass

    def test_should_automatically_end_turn_when_player_has_zero_cards(self):
        """
        Player should not be asked to drop cards if he has no cards in his hand.
        """
        (game, running_game) = self.prepare_game()
        pass


if __name__ == '__main__':
    unittest.main()
