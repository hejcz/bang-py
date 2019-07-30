from src.notifications import DamageReceived, Error, PlayBeerOrDodge, GatlingDamageReceived


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
        if state.current_player.used_bang:
            return Error(state.current_player, Error.CANT_PLAY_2BANGS_IN_1TURN)
        return None

    def execute(self, state):
        target = state.find_player(self.target)
        state.current_player.remove_card("bang")
        state.current_player.used_bang = True
        while True:
            answer = yield PlayBeerOrDodge(target)
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


class GatlingCommand(Command):

    def execute(self, state):
        state.current_player.remove_card("gatling")
        for target in (p for p in state.players if p != state.current_player):
            while True:
                answer = yield PlayBeerOrDodge(target)
                if isinstance(answer, SkipCommand):
                    target.health = target.health - 1
                    yield GatlingDamageReceived(target, 1)
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


class SaloonCommand(Command):

    def execute(self, state):
        state.current_player.remove_card("saloon")
        for player in state.players:
            player.heal_for(1)
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


class StagecoachCommand(Command):

    def execute(self, state):
        state.current_player.remove_card("stagecoach")
        state.give_cards_to(state.current_player, 2)
        yield None


class WellsFargoCommand(Command):

    def execute(self, state):
        state.current_player.remove_card("wells_fargo")
        state.give_cards_to(state.current_player, 3)
        yield None


class PanicCommand(Command):

    def __init__(self, target, card_index) -> None:
        self.target = target
        self.card_index = card_index

    def validate(self, state):
        if state.current_player.name == self.target:
            return Error(state.current_player, Error.PANIC_HIMSELF)
        if self.card_index > len(state.find_player(self.target).cards):
            return Error(state.current_player, Error.CANT_PICK_CARD_ON_GIVEN_INDEX)
        return None

    def execute(self, state):
        target = state.find_player(self.target)
        state.current_player.remove_card("panic")
        stolen_card = target.get_and_remove_card_on_index(self.card_index - 1)
        state.current_player.add_cards([stolen_card])
        yield None


class SkipCommand(Command):

    def execute(self, state):
        yield None


class DropCardsCommand(Command):

    def __init__(self, ids) -> None:
        self.cards_to_remove = ids

    def validate(self, state):
        if len(state.current_player.cards) - len(set(self.cards_to_remove)) > state.current_player.health:
            return Error(state.current_player, Error.TOO_LITTLE_CARDS_DROPPED)
        return None

    def execute(self, state):
        state.current_player.drop_cards(self.cards_to_remove)
        yield None
