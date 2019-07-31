from src.notifications import Error, NoEffect
from src.player import Player, NoSuchCardException


def safe_remove_card(target: Player, card_name: str):
    try:
        target.remove_card(card_name)
        return True
    except NoSuchCardException:
        return False


def no_such_card(player: Player):
    return Error(player, Error.CANT_PLAY_CARD_NOT_IN_HAND)


class Command:

    def validate(self, state):
        return None

    def execute(self, state):
        pass


class SkipCommand(Command):

    def execute(self, state):
        yield NoEffect()


class DropCardsCommand(Command):

    def __init__(self, ids) -> None:
        self.cards_to_remove = ids

    def validate(self, state):
        if len(state.current_player.cards) - len(set(self.cards_to_remove)) > state.current_player.health:
            return Error(state.current_player, Error.TOO_LITTLE_CARDS_DROPPED)
        return None

    def execute(self, state):
        state.current_player.drop_cards(self.cards_to_remove)
        yield NoEffect()


class PickCardCommand(Command):

    def __init__(self, index_to_pick) -> None:
        self.index_to_pick = index_to_pick

    def execute(self, state):
        yield NoEffect()
