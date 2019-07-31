from src.card.beer import BeerCommand
from src.card.dodge import DodgeCommand
from src.commands import Command, safe_remove_card, no_such_card, SkipCommand
from src.notifications import Error, PlayBeerOrDodge, DamageReceivedAndEndTurn


class BangCommand(Command):

    def __init__(self, target) -> None:
        self.target = target

    def validate(self, state):
        if state.current_player.name == self.target:
            return Error(state.current_player, Error.BANG_HIMSELF)
        if state.current_player.used_bang:
            return Error(state.current_player, Error.CANT_PLAY_2BANGS_IN_1TURN)
        return None

    def execute(self, state):
        target = state.find_player(self.target)
        if not safe_remove_card(target, "bang"):
            yield no_such_card(target)
        state.current_player.used_bang = True
        while True:
            answer = yield PlayBeerOrDodge(target)
            if isinstance(answer, SkipCommand):
                target.health = target.health - 1
                yield DamageReceivedAndEndTurn(target, 1)
                return
            elif isinstance(answer, DodgeCommand):
                if not safe_remove_card(target, "dodge"):
                    continue
                break
            elif isinstance(answer, BeerCommand) and target.health == 1:
                if not safe_remove_card(target, "beer"):
                    continue
                break
        yield None
