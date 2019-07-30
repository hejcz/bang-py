class PlayCard:

    def __init__(self, player) -> None:
        self.player = player

    @staticmethod
    def ends_card_effect():
        return False

    @staticmethod
    def requires_response():
        return True


class PlayBeerOrDodge:

    def __init__(self, player) -> None:
        self.player = player

    @staticmethod
    def ends_card_effect():
        return False

    @staticmethod
    def requires_response():
        return True


class DropCards:

    def __init__(self, player) -> None:
        self.player = player

    @staticmethod
    def ends_card_effect():
        return False

    @staticmethod
    def requires_response():
        return True


class DamageReceived:

    def __init__(self, player, value) -> None:
        self.player = player
        self.value = value

    @staticmethod
    def ends_card_effect():
        return True

    @staticmethod
    def requires_response():
        return False


class GatlingDamageReceived:

    def __init__(self, player, value) -> None:
        self.player = player
        self.value = value

    @staticmethod
    def ends_card_effect():
        return False

    @staticmethod
    def requires_response():
        return False


class Error:
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

    @staticmethod
    def requires_response():
        return True
