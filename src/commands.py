from src.notifications import DamageReceivedAndEndTurn, Error, PlayBeerOrDodge, DamageReceived, DropCards, PlayBang, \
    PickCard
from src.player import Player, NoSuchCardException


def safe_remove_card(target: Player, card_name: str):
    try:
        target.remove_card(card_name)
        return True
    except NoSuchCardException:
        return False


def no_such_card(player: Player):
    return Error(player, Error.CANT_PLAY_CARD_NOT_IN_HAND)


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
        if not safe_remove_card(target, "bang"):
            yield no_such_card(target)
        state.current_player.used_bang = True
        while True:
            answer = yield PlayBeerOrDodge(target)
            if isinstance(answer, SkipCommand):
                target.health = target.health - 1
                yield DamageReceivedAndEndTurn(target, 1)
                break
            elif isinstance(answer, DodgeCommand):
                if not safe_remove_card(target, "dodge"):
                    continue
                break
            elif isinstance(answer, BeerCommand) and target.health == 1:
                if not safe_remove_card(target, "beer"):
                    continue
                break
        yield None


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
        yield None


class SaloonCommand(Command):

    def execute(self, state):
        if not safe_remove_card(state.current_player, "saloon"):
            yield no_such_card(state.current_player)
        for player in state.players:
            player.heal_for(1)
        yield None


class BeerCommand(Command):

    def execute(self, state):
        if not safe_remove_card(state.current_player, "beer"):
            yield no_such_card(state.current_player)
        state.current_player.heal_for(1)
        yield None


class DodgeCommand(Command):

    def execute(self, state):
        if not safe_remove_card(state.current_player, "dodge"):
            yield no_such_card(state.current_player)
        yield None


class StagecoachCommand(Command):

    def execute(self, state):
        if not safe_remove_card(state.current_player, "stagecoach"):
            yield no_such_card(state.current_player)
        state.give_cards_to(state.current_player, 2)
        yield None


class WellsFargoCommand(Command):

    def execute(self, state):
        if not safe_remove_card(state.current_player, "wells_fargo"):
            yield no_such_card(state.current_player)
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
        if not safe_remove_card(state.current_player, "panic"):
            yield no_such_card(state.current_player)
        target = state.find_player(self.target)
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


class PickCardCommand(Command):

    def __init__(self, index_to_pick) -> None:
        self.index_to_pick = index_to_pick

    def execute(self, state):
        yield None


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


class ShopCommand(Command):

    def execute(self, state):
        if not safe_remove_card(state.current_player, "shop"):
            yield no_such_card(state.current_player)
        current_player_index = state.players.index(state.current_player)
        ordered_players = state.players[current_player_index:] + state.players[:current_player_index]
        cards_in_shop = state.pop_cards(len(state.players))
        for target in ordered_players:
            while True:
                answer = yield PickCard(target, cards_in_shop)
                if isinstance(answer, PickCardCommand):
                    if answer.index_to_pick > len(cards_in_shop):
                        continue
                    target.add_cards([cards_in_shop[answer.index_to_pick - 1]])
                    cards_in_shop.pop(answer.index_to_pick - 1)
                    break
        yield None


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
