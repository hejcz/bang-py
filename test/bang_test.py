import unittest

from src.channel import Channel
from src.commands import BangCommand, SkipCommand, BeerCommand, DropCardsCommand as DropCardsCommand, PanicCommand
from src.game import Game
from src.notifications import Error, DropCards, PlayBeerOrDodge, PlayCard


class TestChannel(Channel):

    def __init__(self) -> None:
        super().__init__()


class TestSum(unittest.TestCase):

    @staticmethod
    def six_bangs():
        return ["bang", "bang", "bang", "bang", "bang", "bang"]

    @staticmethod
    def prepare_game(cards, players=None):
        if players is None:
            players = ["tom", "julian"]
        game = Game(TestChannel(), players, cards)
        running_game = game.game_runner()
        running_game.send(None)
        return game, running_game

    def test_player_cant_bang_himself(self):
        (game, running_game) = self.prepare_game(self.six_bangs())
        self.assertEqual(game.state.current_player.health, 4, "should be equal to initial value")
        step = running_game.send(BangCommand("tom"))
        self.assert_error(step, Error.BANG_HIMSELF)

    def test_cant_play_card_that_he_has_not_in_hand(self):
        (game, running_game) = self.prepare_game(self.six_bangs())
        step = running_game.send(BeerCommand())
        self.assert_error(step, Error.CANT_PLAY_CARD_NOT_IN_HAND)

    def test_must_drop_cards_if_he_has_more_cards_than_hp(self):
        """
        If player has 1 health and 4 cards then he must drop cards.
        """
        (game, running_game) = self.prepare_game(self.six_bangs())
        game.state.current_player.health = 3
        step = running_game.send(SkipCommand())
        self.assert_notification(step, DropCards, game.state.players[0])

    def test_must_drop_enough_cards(self):
        """
        If player has 1 health and 4 cards then he must drop cards.
        """
        (game, running_game) = self.prepare_game(self.six_bangs())
        game.state.current_player.health = 1
        running_game.send(SkipCommand())
        step = running_game.send(DropCardsCommand([1]))
        self.assert_error(step, Error.TOO_LITTLE_CARDS_DROPPED)

    def test_must_drop_enough_cards_2(self):
        """
        If player has 1 health and 4 cards then he must drop cards.
        """
        (game, running_game) = self.prepare_game(self.six_bangs())
        game.state.current_player.health = 1
        running_game.send(SkipCommand())
        step = running_game.send(DropCardsCommand([1, 2, 3]))
        self.assert_notification(step, PlayCard, game.state.players[1])

    def test_must_drop_cards_if_he_has_more_cards_than_hp_2(self):
        """
        If player has 1 health and 4 cards then he must drop cards.
        """
        (game, running_game) = self.prepare_game(self.six_bangs())
        game.state.current_player.health = 4
        step = running_game.send(SkipCommand())
        self.assert_notification(step, PlayCard, game.state.players[1])

    def test_should_automatically_end_turn_when_player_has_zero_cards(self):
        """
        Player should not be asked to drop cards if he has less card on hand than hp.
        """
        (game, running_game) = self.prepare_game(self.six_bangs())
        step = running_game.send(SkipCommand())
        self.assert_notification(step, PlayCard, game.state.players[1])

    def test_play_bang_on_self_then_on_enemy(self):
        """
        Player should not be asked to drop cards if he has less card on hand than hp.
        """
        (game, running_game) = self.prepare_game(self.six_bangs())
        running_game.send(BangCommand("tom"))
        # player should repeat his invalid move
        running_game.send(None)  # swallow error
        step = running_game.send(BangCommand("julian"))
        self.assert_notification(step, PlayBeerOrDodge, game.state.players[1])

    def test_panic(self):
        """
        Target should loose 1 card and current player should receive one card
        """
        (game, running_game) = self.prepare_game(["panic", "bang", "beer", "beer", "bang", "bang"])
        running_game.send(PanicCommand("julian", 1))
        self.assertEqual(1, len(game.state.find_player("julian").cards), "Julian lost 1 card")
        self.assertEqual(4, len(game.state.find_player("tom").cards), "Tom received 1 card (he spent panic though)")

    def test_panic_cant_be_played_on_self(self):
        (game, running_game) = self.prepare_game(["panic", "bang", "beer", "beer", "bang", "bang"])
        step = running_game.send(PanicCommand("tom", 1))
        self.assert_error(step, Error.PANIC_HIMSELF)

    def test_panic_player_cant_select_index_of_card_player_does_not_have_on_hand(self):
        (game, running_game) = self.prepare_game(["panic", "bang", "beer", "beer", "bang", "bang"])
        step = running_game.send(PanicCommand("julian", 100))
        self.assert_error(step, Error.CANT_PICK_CARD_ON_GIVEN_INDEX)

    def assert_error(self, step, error):
        self.assertIsInstance(step["content"], Error, "should be error")
        self.assertEqual(step["content"].error, error, "should have expected reason")

    def assert_notification(self, step, cls, players):
        self.assertIsInstance(step["content"], cls, "should be info")
        self.assertEqual(step["content"].player, players, "should concern expected player")


if __name__ == '__main__':
    unittest.main()
