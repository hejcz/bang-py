class Info:

    PLAY_CARD = 0
    BANG_OR_DODGE = 1
    REMOVE_CARDS = 2

    def __init__(self, player, msg) -> None:
        self.player = player
        self.msg = msg


class DamageReceived:

    def __init__(self, player, value) -> None:
        self.player = player
        self.value = value


class Error:

    def __init__(self, player, error) -> None:
        self.player = player
        self.error = error
