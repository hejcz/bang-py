from typing import Dict
import re


class Channel:
    """
    Abstraction over sending game events and receiving players commands.
    It's implementation might be mocked for tests, print to console and read standard output
    or use websockets.
    """

    def send(self, msg: Dict[str, str]):
        pass

    async def receive(self) -> Dict[str, str]:
        pass


def bang_adapter(command):
    matches = re.search("^play bang on ([^ ]+)$", command)
    if matches is None:
        return None
    target = matches.group(1)
    if target is None:
        return None
    return {"type": "card", "name": "bang", "target": target}


def skip_adapter(command):
    if command == "skip":
        return {"type": "skip"}
    return None


def play_card_without_target_adapter(command):
    matches = re.search("^play ([^ ]+)$", command)
    if matches is None:
        return None
    card_name = matches.group(1)
    if card_name is None:
        return None
    return {"type": "card", "name": card_name}


def drop_cards_adapter(command):
    matches = re.search("^drop (.+)$", command)
    if matches is None:
        return None
    try:
        ids = map(lambda num: int(num), re.split(",", matches.group(1)))
        return {"type": "drop_cards", "ids": ids}
    except Exception:
        return None


class TerminalChannel(Channel):
    adapters = [
        bang_adapter,
        skip_adapter,
        play_card_without_target_adapter,
        drop_cards_adapter
    ]

    def send(self, msg: Dict[str, str]):
        if msg.get("type") == "info":
            print("[{}]: {}".format(msg["player"], msg["msg"]))
        elif msg.get("effect") == "damage":
            print("[{}]: you received {} damage!".format(msg["player"], msg["value"]))
        elif msg.get("type") == "error":
            print("[{}]: don't cheat, you {}!".format(msg["player"], msg["msg"]))

    async def receive(self):
        player_input = input().strip()
        command = next(match(player_input) for match in self.adapters if match(player_input) is not None)
        return command
