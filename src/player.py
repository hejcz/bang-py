from typing import List


class NoSuchCardException(Exception):

    def __init__(self, card_id, *args: object) -> None:
        super().__init__(*args)
        self.card_id = card_id


class Player:

    def __init__(self, name) -> None:
        self.name: str = name
        self.health: int = 4
        self.used_bang: bool = False
        self.cards: List[str] = []

    def add_cards(self, ids):
        self.cards = self.cards + ids

    def remove_card(self, card_id):
        try:
            self.cards.remove(card_id)
        except ValueError:
            raise NoSuchCardException(card_id)

    def get_and_remove_card_on_index(self, card_index):
        return self.cards.pop(card_index)

    def drop_cards(self, ids):
        self.cards = [card for j, card in enumerate(self.cards) if j + 1 not in ids]

    def heal_for(self, value):
        self.health = self.health + value

    def __str__(self) -> str:
        return "[{}] >> health: {}, cards: {}".format(self.name, self.health, self.cards)
