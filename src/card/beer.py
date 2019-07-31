from src.commands import Command, safe_remove_card, no_such_card


class BeerCommand(Command):

    def execute(self, state):
        if not safe_remove_card(state.current_player, "beer"):
            yield no_such_card(state.current_player)
        state.current_player.heal_for(1)
        yield None
