class SendsSomethingMixin:

    @staticmethod
    def has_something_to_send():
        return True


class RequiresResponseMixin:

    @staticmethod
    def requires_response():
        return True


class PlayCard(SendsSomethingMixin, RequiresResponseMixin):

    def __init__(self, player) -> None:
        self.player = player

    @staticmethod
    def ends_card_effect():
        return False


class PlayBeerOrDodge(SendsSomethingMixin, RequiresResponseMixin):

    def __init__(self, player) -> None:
        self.player = player

    @staticmethod
    def ends_card_effect():
        return False


class DropCards(SendsSomethingMixin, RequiresResponseMixin):

    def __init__(self, player) -> None:
        self.player = player

    @staticmethod
    def ends_card_effect():
        return False


class DamageReceivedAndEndTurn(SendsSomethingMixin):

    def __init__(self, player, value) -> None:
        self.player = player
        self.value = value

    @staticmethod
    def ends_card_effect():
        return True

    @staticmethod
    def requires_response():
        return False


class DamageReceived(SendsSomethingMixin):

    def __init__(self, player, value) -> None:
        self.player = player
        self.value = value

    @staticmethod
    def ends_card_effect():
        return False

    @staticmethod
    def requires_response():
        return False


class Error(SendsSomethingMixin, RequiresResponseMixin):
    BANG_HIMSELF = 0
    TOO_LITTLE_CARDS_DROPPED = 1
    CANT_PLAY_CARD_NOT_IN_HAND = 2
    CANT_PLAY_2BANGS_IN_1TURN = 3
    PANIC_HIMSELF = 4
    CANT_PICK_CARD_ON_GIVEN_INDEX = 5

    def __init__(self, player, error) -> None:
        self.player = player
        self.error = error

    @staticmethod
    def ends_card_effect():
        return False


class PlayBang(SendsSomethingMixin, RequiresResponseMixin):

    def __init__(self, player) -> None:
        self.player = player

    @staticmethod
    def ends_card_effect():
        return False


class PickCard(SendsSomethingMixin, RequiresResponseMixin):

    def __init__(self, player, cards) -> None:
        self.player = player
        self.cards = cards

    @staticmethod
    def ends_card_effect():
        return False


class NoEffect:

    @staticmethod
    def ends_card_effect():
        return True

    @staticmethod
    def requires_response():
        return False

    @staticmethod
    def has_something_to_send():
        return False
