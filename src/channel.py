import re
from typing import Dict

from src.commands import Command, DodgeCommand, BeerCommand, BangCommand, DropCardsCommand, SkipCommand, \
    StagecoachCommand, WellsFargoCommand, PanicCommand, SaloonCommand, GatlingCommand, IndiansCommand, ShopCommand, \
    KateCommand, DuelCommand, PickCardCommand
from src.notifications import DamageReceivedAndEndTurn, Error, DropCards, PlayBeerOrDodge, PlayCard, PlayBang, PickCard


class Channel:
    """
    Abstraction over sending game events and receiving players commands.
    It's implementation might be mocked for tests, print to console and read standard output
    or use websockets.
    """

    def send(self, msg: Dict[str, str]):
        pass

    async def receive(self) -> Command:
        pass


def bang_adapter(command):
    matches = re.search("^play ([^ ]+) on ([^ ]+)$", command)
    if matches is None:
        return None
    card = matches.group(1)
    if card is None:
        return None
    target = matches.group(2)
    if target is None:
        return None
    if card == "bang":
        return BangCommand(target)
    if card == "kate":
        return KateCommand(target)
    if card == "duel":
        return DuelCommand(target)
    return None


def panic_adapter(command):
    matches = re.search("^play panic on ([^ ]+) and pick (\\d+)$", command)
    if matches is None:
        return None
    target = matches.group(1)
    if target is None:
        return None
    card_index = matches.group(2)
    if card_index is None:
        return None
    return PanicCommand(target, int(card_index))


def skip_adapter(command):
    if command == "skip":
        return SkipCommand()
    return None


def play_card_without_target_adapter(command):
    matches = re.search("^play ([^ ]+)$", command)
    if matches is None:
        return None
    card_name = matches.group(1)
    if card_name is None:
        return None
    if card_name == "beer":
        return BeerCommand()
    if card_name == "dodge":
        return DodgeCommand()
    if card_name == "stagecoach":
        return StagecoachCommand()
    if card_name == "wells_fargo":
        return WellsFargoCommand()
    if card_name == "saloon":
        return SaloonCommand()
    if card_name == "gatling":
        return GatlingCommand()
    if card_name == "indians":
        return IndiansCommand()
    if card_name == "shop":
        return ShopCommand()
    return None


def drop_cards_adapter(command):
    matches = re.search("^drop (.+)$", command)
    if matches is None:
        return None
    try:
        ids = list(map(lambda num: int(num), re.split(",", matches.group(1))))
        return DropCardsCommand(ids)
    except Exception:
        return None


def pick_cards_adapter(command):
    matches = re.search("^pick (\\d)$", command)
    if matches is None:
        return None
    try:
        ids = int(matches.group(1))
        return PickCardCommand(ids)
    except Exception:
        return None


class TerminalChannel(Channel):
    adapters = [
        bang_adapter,
        skip_adapter,
        play_card_without_target_adapter,
        drop_cards_adapter,
        panic_adapter,
        pick_cards_adapter
    ]

    error_mappings = {
        Error.BANG_HIMSELF: "You can't play bang on yourself!",
        Error.TOO_LITTLE_CARDS_DROPPED: "Drop more cards. You can have at most number of cards equal to your health",
        Error.CANT_PLAY_CARD_NOT_IN_HAND: "You can only play cards you have on your hand!",
        Error.CANT_PLAY_2BANGS_IN_1TURN: "You can only play one bang during your turn!",
        Error.PANIC_HIMSELF: "You can't play panic on yourself!",
        Error.CANT_PICK_CARD_ON_GIVEN_INDEX: "You can't get chosen card because player does not have it!"
    }

    def send(self, notification):
        if isinstance(notification, PlayCard):
            print("[{}]: Play card!".format(notification.player))
        if isinstance(notification, PlayBeerOrDodge):
            print("[{}]: Avoid bang!".format(notification.player))
        if isinstance(notification, DropCards):
            print("[{}]: Remove cards e.g. 1,2 to remove first and second cards!".format(notification.player))
        elif isinstance(notification, DamageReceivedAndEndTurn):
            print("[{}]: you received {} damage!".format(notification.player, notification.value))
        elif isinstance(notification, PlayBang):
            print("[{}]: play bang!".format(notification.player))
        elif isinstance(notification, PickCard):
            print("[{}]: pick card out of {} e.g. \"pick 1\"!".format(notification.player, notification.cards))
        elif isinstance(notification, Error):
            print("[ERROR][{}]: {}!".format(notification.player, self.error_mappings[notification.error]))

    async def receive(self):
        """
        Valid commands:
        1. play bang on player_name
        2. play beer
        3. play dodge
        4. skip - don't use dodge/beer on bang or end turn
        5. drop 1 / drop 1,2 - drop cards on indices
        """
        while True:
            player_input = input().strip()
            try:
                command = next(cmd for cmd in (match(player_input) for match in self.adapters) if cmd is not None)
                break
            except StopIteration:
                print("That was not a valid command. Try again!")
        return command
