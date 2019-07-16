from typing import List


class Player:

    def __init__(self, name) -> None:
        self.name: str = name
        self.health: int = 4
        self.used_bang: bool = False
        self.cards: List[str] = []

    def add_cards(self, ids):
        self.cards = self.cards + ids

    def remove_card(self, id):
        self.cards.remove(id)

    def drop_cards(self, ids):
        self.cards = [card for j, card in enumerate(self.cards) if j not in ids]

    def heal_for(self, value):
        self.health = self.health + value

    def __str__(self) -> str:
        return "[{}] >> health: {}, cards: {}".format(self.name, self.health, self.cards)