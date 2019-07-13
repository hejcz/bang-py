import asyncio
from typing import List

from channel import Channel, TerminalChannel


class Player:
    name: str
    health: int = 4
    used_bang: bool = False
    cards: List[str] = []

    def __init__(self, name) -> None:
        self.name = name

    def add_cards(self, ids):
        self.cards = self.cards + ids

    def remove_card(self, id):
        self.cards.remove(id)

    def drop_cards(self, ids):
        self.cards = [card for j, card in self.cards if j not in ids]

    def heal_for(self, value):
        self.health = self.health + value

    def __str__(self) -> str:
        return "[{}] >> health: {}, cards: {}".format(self.name, self.health, self.cards)


class State:
    players: List[Player] = []
    current_player: Player = None

    def __init__(self, players) -> None:
        self.players = players
        self.current_player = players[-1]

    def end_turn(self):
        self.current_player.used_bang = False
        (_, idx) = divmod(self.players.index(self.current_player) + 1, len(self.players))
        self.current_player = self.players[idx]

    def is_game_finished(self):
        return len([p for p in self.players if p.health > 0]) == 1


def bang(command, state):
    target = next(p for p in state.players if p.name == command["target"])
    state.current_player.remove_card("bang")
    target_response = yield {"player": target, "type": "info", "msg": "you can play dodge or beer"}
    if target_response.get("type") == "skip":
        target.health = target.health - 1
        yield {"type": "finish", "effect": "damage", "player": target, "value": 1}
    elif target_response.get("type") == "card" and target_response.get("name") == "dodge":
        target.remove_card("dodge")
        yield None
    elif target_response.get("type") == "card" and target_response.get("name") == "beer" and target.health == 1:
        target.remove_card("beer")
        yield None


def beer(command, state):
    state.current_player.remove_card("beer")
    state.current_player.heal_for(1)
    yield None


def dodge(command, state):
    state.current_player.remove_card("dodge")
    yield None


def command_to_generator(command, state):
    if command.get("type") == "card":
        if command.get("name") == "bang":
            return bang(command, state)
        if command.get("name") == "beer":
            return beer(command, state)
        if command.get("name") == "dodge":
            return dodge(command, state)


class Game:
    state = State([Player("tom"), Player("julian")])

    def __init__(self, channel: Channel):
        self.channel = channel

    async def start(self):
        running_game = self.game_runner()
        step = running_game.send(None)
        while True:
            if step is None:
                break
            if step.get("only_send", False):
                self.channel.send(step["content"])
                step = running_game.send(None)
            if step.get("send_and_receive", False):
                self.channel.send(step["content"])
                received = await self.channel.receive()
                step = running_game.send(received)

    @staticmethod
    def send_and_receive(content):
        return {"send_and_receive": True, "content": content}

    @staticmethod
    def just_send(content):
        return {"just_send": True, "content": content}

    def game_runner(self):
        self.state.end_turn()
        for player in self.state.players:
            player.add_cards(["bang", "dodge"])
        while not self.state.is_game_finished():
            # phase 1
            self.state.current_player.add_cards(["bang", "dodge"])

            # phase 2
            while True:
                command = yield self.send_and_receive(
                    {'type': "info", 'player': self.state.current_player, 'msg': "play card!"})
                if command.get("type") == "skip":
                    break
                current_card = command_to_generator(command, self.state)
                step = current_card.send(None)  # start it
                while step is not None:
                    action = yield self.send_and_receive(step)
                    step = current_card.send(action)
                    if step is None:
                        break
                    if step.get("type") == "finish":
                        yield self.just_send(step)
                        break

            # phase 3
            cards_to_remove = yield self.send_and_receive(
                {'type': "info", 'player': self.state.current_player,
                 'msg': "remove cards e.g. 1,2 to remove first and second cards"})
            self.state.current_player.drop_cards(cards_to_remove)
            self.state.end_turn()


asyncio.run(Game(TerminalChannel()).start())
