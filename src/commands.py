from src.notifications import DamageReceived, Error, PlayBangOrDodge


class Command:

    def validate(self, state):
        return None

    def execute(self, state):
        pass


class BangCommand(Command):

    def __init__(self, target) -> None:
        self.target = target

    def validate(self, state):
        if state.current_player.name == self.target:
            return Error(state.current_player, Error.BANG_HIMSELF)
        return None

    def execute(self, state):
        target = next(p for p in state.players if p.name == self.target)
        state.current_player.remove_card("bang")
        while True:
            answer = yield PlayBangOrDodge(target)
            if isinstance(answer, SkipCommand):
                target.health = target.health - 1
                yield DamageReceived(target, 1)
                break
            elif isinstance(answer, DodgeCommand):
                target.remove_card("dodge")
                break
            elif isinstance(answer, BeerCommand) and target.health == 1:
                target.remove_card("beer")
                break
            else:
                pass
        yield None


class BeerCommand(Command):

    def execute(self, state):
        state.current_player.remove_card("beer")
        state.current_player.heal_for(1)
        yield None


class DodgeCommand(Command):

    def execute(self, state):
        state.current_player.remove_card("dodge")
        yield None


class SkipCommand(Command):

    def execute(self, state):
        yield None


class DropCardsCommand(Command):

    def __init__(self, ids) -> None:
        self.ids = ids

    def validate(self, state):
        if len(state.current_player.cards) - len(self.ids) > state.current_player.health:
            yield Error(state.current_player, Error.TOO_LITTLE_CARDS_DROPPED)
        return None

    def execute(self, state):
        state.current_player.drop_cards(self.ids)
        yield None
