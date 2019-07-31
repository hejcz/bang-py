from src.commands import Command, safe_remove_card, no_such_card, PickCardCommand
from src.notifications import PickCard


class ShopCommand(Command):

    def execute(self, state):
        if not safe_remove_card(state.current_player, "shop"):
            yield no_such_card(state.current_player)
        current_player_index = state.players.index(state.current_player)
        ordered_players = state.players[current_player_index:] + state.players[:current_player_index]
        cards_in_shop = state.pop_cards(len(state.players))
        for target in ordered_players:
            while True:
                answer = yield PickCard(target, cards_in_shop)
                if isinstance(answer, PickCardCommand):
                    if answer.index_to_pick > len(cards_in_shop):
                        continue
                    target.add_cards([cards_in_shop[answer.index_to_pick - 1]])
                    cards_in_shop.pop(answer.index_to_pick - 1)
                    break
        yield None
