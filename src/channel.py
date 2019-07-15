from typing import Dict
import re

from src.commands import Command, DodgeCommand, BeerCommand, BangCommand, DropCards, SkipCommand
from src.notifications import Info, DamageReceived, Error


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
    matches = re.search("^play bang on ([^ ]+)$", command)
    if matches is None:
        return None
    target = matches.group(1)
    if target is None:
        return None
    return BangCommand(target)


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


def drop_cards_adapter(command):
    matches = re.search("^drop (.+)$", command)
    if matches is None:
        return None
    try:
        ids = map(lambda num: int(num), re.split(",", matches.group(1)))
        return DropCards(ids)
    except Exception:
        return None


class TerminalChannel(Channel):
    adapters = [
        bang_adapter,
        skip_adapter,
        play_card_without_target_adapter,
        drop_cards_adapter
    ]

    info_mappings = {
        Info.PLAY_CARD: "play card!",
        Info.BANG_OR_DODGE: "you can play dodge or beer",
        Info.REMOVE_CARDS: "remove cards e.g. 1,2 to remove first and second cards"
    }

    def send(self, notification):
        if isinstance(notification, Info):
            print("[{}]: {}".format(notification.player, self.info_mappings[notification.msg]))
        elif isinstance(notification, DamageReceived):
            print("[{}]: you received {} damage!".format(notification.player, notification.value))
        elif isinstance(notification, Error):
            print("[{}]: don't cheat. {}!".format(notification.player, notification.error))

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
                command = next(match(player_input) for match in self.adapters if match(player_input) is not None)
                break
            except StopIteration:
                print("That was not a valid command. Try again!")
        return command
