from src.commands import Command, safe_remove_card, no_such_card
from src.notifications import Error


class PanicCommand(Command):

    def __init__(self, target, card_index) -> None:
        self.target = target
        self.card_index = card_index

    def validate(self, state):
        if state.current_player.name == self.target:
            return Error(state.current_player, Error.PANIC_HIMSELF)
        if self.card_index > len(state.find_player(self.target).cards):
            return Error(state.current_player, Error.CANT_PICK_CARD_ON_GIVEN_INDEX)
        return None

    def execute(self, state):
        if not safe_remove_card(state.current_player, "panic"):
            yield no_such_card(state.current_player)
        target = state.find_player(self.target)
        stolen_card = target.get_and_remove_card_on_index(self.card_index - 1)
        state.current_player.add_cards([stolen_card])
        yield None
