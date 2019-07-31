from src.commands import Command, safe_remove_card, no_such_card


class SaloonCommand(Command):

    def execute(self, state):
        if not safe_remove_card(state.current_player, "saloon"):
            yield no_such_card(state.current_player)
        for player in state.players:
            player.heal_for(1)
        yield None
