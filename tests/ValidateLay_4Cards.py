import os, sys

cur_dir = os.path.dirname(os.path.abspath(__file__))
parent_dir = os.path.dirname(cur_dir)
sys.path.append(parent_dir)

from minimise import Card, JokerCard, GameManager

class ValidateLay_4Cards:

    def __init__(self):
        pass

    def assert_equals(self, cards_list, joker_card, expected_op):
        actual_op = GameManager.validate_lay(cards_list, joker_card)
        return actual_op == expected_op

    def quadruplet(self):
        pass

    def sequence_without_joker(self):
        pass

    def sequence_with_joker(self):
        pass

    def all_jokers(self):
        pass

    def failure(self):
        pass
