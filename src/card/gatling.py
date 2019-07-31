from src.card.beer import BeerCommand
from src.card.dodge import DodgeCommand
from src.commands import Command, safe_remove_card, no_such_card, SkipCommand
from src.notifications import PlayBeerOrDodge, DamageReceived, NoEffect


class GatlingCommand(Command):

    def execute(self, state):
        if not safe_remove_card(state.current_player, "gatling"):
            yield no_such_card(state.current_player)
        for target in (p for p in state.players if p != state.current_player):
            while True:
                answer = yield PlayBeerOrDodge(target)
                if isinstance(answer, SkipCommand):
                    target.health = target.health - 1
                    yield DamageReceived(target, 1)
                    break
                elif isinstance(answer, DodgeCommand):
                    if not safe_remove_card(state.current_player, "dodge"):
                        continue
                    break
                elif isinstance(answer, BeerCommand) and target.health == 1:
                    if not safe_remove_card(state.current_player, "beer"):
                        continue
                    break
        yield NoEffect()
