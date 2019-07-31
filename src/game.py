from src.channel import Channel
from src.commands import SkipCommand
from src.notifications import PlayCard, DropCards
from src.player import Player
from src.state import State


class Game:

    def __init__(self, channel: Channel, players, cards):
        self.state = State([Player(name) for name in players], cards)
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
            self.state.give_cards_to(player, 2)
        while not self.state.is_game_finished():
            # phase 1
            self.state.give_cards_to(self.state.current_player, 2)

            # phase 2
            while len(self.state.current_player.cards) > 0:
                # play card
                command = yield self.send_and_receive(PlayCard(self.state.current_player))

                # end turn
                if isinstance(command, SkipCommand):
                    break

                # check if command is valid
                validate = command.validate(self.state)
                if validate is not None:
                    yield self.just_send(validate)
                    continue

                cmd_runner = command.execute(self.state)
                action = None
                while True:
                    step = cmd_runner.send(action)
                    # all card effects have been applied
                    if step.ends_card_effect():
                        if step.has_something_to_send():
                            yield self.just_send(step)
                        break
                    # card still has some effects to consider and requires some player to interact
                    if step.requires_response():
                        action = yield self.send_and_receive(step)
                    # card still has some effects to consider but it does not require interaction
                    else:
                        yield self.just_send(step)

            # phase 3
            if len(self.state.current_player.cards) > self.state.current_player.health:
                while True:
                    drop_cards_command = yield self.send_and_receive(DropCards(self.state.current_player))
                    validate = drop_cards_command.validate(self.state)
                    if validate is not None:
                        yield self.just_send(validate)
                        continue
                    drop_cards_command.execute(self.state).send(None)
                    break

            self.state.end_turn()
