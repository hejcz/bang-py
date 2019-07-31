from src.card.bang import BangCommand
from src.commands import Command, safe_remove_card, no_such_card, SkipCommand
from src.notifications import PlayBang, DamageReceived


class IndiansCommand(Command):

    def execute(self, state):
        if not safe_remove_card(state.current_player, "indians"):
            yield no_such_card(state.current_player)
        for target in (p for p in state.players if p != state.current_player):
            while True:
                answer = yield PlayBang(target)
                if isinstance(answer, SkipCommand):
                    target.health = target.health - 1
                    yield DamageReceived(target, 1)
                    break
                elif isinstance(answer, BangCommand):
                    if not safe_remove_card(state.current_player, "bang"):
                        continue
                    break
        yield None
