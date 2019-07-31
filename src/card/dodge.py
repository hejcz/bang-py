from src.commands import Command, safe_remove_card, no_such_card


class DodgeCommand(Command):

    def execute(self, state):
        if not safe_remove_card(state.current_player, "dodge"):
            yield no_such_card(state.current_player)
        yield None
