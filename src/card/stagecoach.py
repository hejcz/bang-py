from src.commands import Command, safe_remove_card, no_such_card
from src.notifications import NoEffect


class StagecoachCommand(Command):

    def execute(self, state):
        if not safe_remove_card(state.current_player, "stagecoach"):
            yield no_such_card(state.current_player)
        state.give_cards_to(state.current_player, 2)
        yield NoEffect()
