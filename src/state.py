from typing import List

from src.player import Player


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