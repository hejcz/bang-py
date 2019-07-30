class State:

    def __init__(self, players, cards) -> None:
        self.players = players
        self.cards = cards
        self.current_player = players[-1]

    def end_turn(self):
        self.current_player.used_bang = False
        (_, idx) = divmod(self.players.index(self.current_player) + 1, len(self.players))
        self.current_player = self.players[idx]

    def is_game_finished(self):
        return len([p for p in self.players if p.health > 0]) == 1

    def give_cards_to(self, player, how_many):
        player.add_cards(self.cards[0:how_many])
        self.cards = self.cards[how_many:]

    def find_player(self, name):
        return next(p for p in self.players if p.name == name)
