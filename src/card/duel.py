from src.card.bang import BangCommand
from src.commands import Command, safe_remove_card, no_such_card, SkipCommand
from src.notifications import PlayBang, DamageReceivedAndEndTurn
from src.player import Player


class DuelCommand(Command):

    def __init__(self, target) -> None:
        self.target = target

    def execute(self, state):
        if not safe_remove_card(state.current_player, "duel"):
            yield no_such_card(state.current_player)
        target_player = state.find_player(self.target)
        next_player: Player = target_player
        while True:
            answer = yield PlayBang(next_player)
            if isinstance(answer, SkipCommand):
                next_player.health = next_player.health - 1
                yield DamageReceivedAndEndTurn(next_player, 1)
            if isinstance(answer, BangCommand):
                if not safe_remove_card(next_player, "bang"):
                    continue
                next_player = state.current_player if next_player == target_player else target_player
