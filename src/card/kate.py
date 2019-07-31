from src.commands import Command, safe_remove_card, no_such_card, DropCardsCommand
from src.notifications import DropCards


class KateCommand(Command):

    def __init__(self, target) -> None:
        self.target = target

    def execute(self, state):
        if not safe_remove_card(state.current_player, "kate"):
            yield no_such_card(state.current_player)
        target_player = state.find_player(self.target)
        while True:
            answer = yield DropCards(target_player)
            if isinstance(answer, DropCardsCommand):
                if len(answer.cards_to_remove) != 1:
                    continue
                target_player.drop_cards(answer.cards_to_remove)
                break
        yield None
