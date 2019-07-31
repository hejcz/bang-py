from src.commands import Command, safe_remove_card, no_such_card
from src.notifications import NoEffect


class WellsFargoCommand(Command):

    def execute(self, state):
        if not safe_remove_card(state.current_player, "wells_fargo"):
            yield no_such_card(state.current_player)
        state.give_cards_to(state.current_player, 3)
        yield NoEffect()
