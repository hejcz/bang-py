from src.channel import Channel
from src.notifications import Info, DamageReceived, Error
from src.player import Player, NoSuchCardException
from src.state import State


class Game:

    def __init__(self, channel: Channel):
        self.state = State([Player("tom"), Player("julian")])
        self.channel = channel

    async def start(self):
        running_game = self.game_runner()
        step = running_game.send(None)
        while True:
            if step is None:
                break
            elif step.get("just_send", False):
                self.channel.send(step["content"])
                step = running_game.send(None)
            elif step.get("send_and_receive", False):
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
                command = yield self.send_and_receive(Info(self.state.current_player, Info.PLAY_CARD))
                cmd_runner = command.execute(self.state)
                try:
                    step = cmd_runner.send(None)
                except NoSuchCardException:
                    yield self.just_send(Error(self.state.current_player, Error.CANT_PLAY_CARD_NOT_IN_HAND))
                    continue
                if step is None:
                    break
                if isinstance(step, Error):
                    yield self.just_send(step)
                    continue
                while step is not None:
                    action = yield self.send_and_receive(step)
                    step = cmd_runner.send(action)
                    if step is None:
                        break
                    if isinstance(step, Error):
                        yield self.just_send(step)
                        continue
                    if isinstance(step, DamageReceived):
                        yield self.just_send(step)
                        break

            # phase 3
            if len(self.state.current_player.cards) > self.state.current_player.health:
                drop_cards_command = yield self.send_and_receive(Info(self.state.current_player, Info.REMOVE_CARDS))
                step = drop_cards_command.execute(self.state).send(None)
                if step is not None:
                    yield self.just_send(step)
            self.state.end_turn()
