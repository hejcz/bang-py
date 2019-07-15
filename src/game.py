from src.channel import Channel
from src.notifications import Info
from src.player import Player
from src.state import State


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
            if step.get("just_send", False):
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
                command = yield self.send_and_receive(Info(self.state.current_player, Info.PLAY_CARD))
                cmd_runner = command.execute(self.state)
                step = cmd_runner.send(None)  # start it
                if step is None:
                    break
                while step is not None:
                    action = yield self.send_and_receive(step)
                    step = cmd_runner.send(action)
                    if step is None:
                        break
                    if step.get("type") == "finish":
                        yield self.just_send(step)
                        break

            # phase 3
            drop_cards_command = yield self.send_and_receive(Info(self.state.current_player, Info.REMOVE_CARDS))
            drop_cards_command.execute(self.state).send(None)
            self.state.end_turn()
