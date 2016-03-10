import os, sys

cur_dir = os.path.dirname(os.path.abspath(__file__))
parent_dir = os.path.dirname(cur_dir)
sys.path.append(parent_dir)

from minimise import Card, JokerCard, GameManager

__all__ = [
    'ValidateLay_3Cards'
]

class ValidateLay_3Cards():

    def __init__(self):
        self.triplet()
        self.sequence_without_joker()
        self.sequence_with_joker()
        self.all_jokers()
        self.failure()

    def assert_equals(self, cards_list, joker_card, expected_op):
        actual_op = GameManager.validate_lay(cards_list, joker_card)
        return actual_op == expected_op

    def triplet(self):
        joker_card = Card('HEARTS', 10)

        card1 = Card('SPADE', 5)
        card2 = Card('CLOVER', 5)
        card3 = Card('HEARTS',5)

        cards_list = [card1, card2, card3]

        case1 = self.assert_equals(cards_list, joker_card, True)

        if not case1:
            print "------------------ triplet failed!"
        else:
            print "triplet succeeded!"

    def sequence_without_joker(self):
        joker_card = Card('HEARTS', 9)

        card1 = Card('SPADE', 5)
        card2 = Card('SPADE', 6)
        card3 = Card('SPADE', 7)

        cards_list = [card1, card2, card3]

        case1 = self.assert_equals(cards_list, joker_card, True)

        card1 = Card('SPADE', 10)
        card2 = Card('SPADE', 'J')
        card3 = Card('SPADE', 'Q')

        cards_list = [card1, card2, card3]

        case2 = self.assert_equals(cards_list, joker_card, True)

        if not case1 or not case2:
            print "------------------ sequence_without_joker failed!"
            print case1, case2
        else:
            print "sequence_without_joker succeeded!"

    def sequence_with_joker(self):
        joker_card = Card('HEARTS', 9)

        # 1 joker
        card1 = Card('SPADE', 5)
        card2 = Card('HEARTS', 9)
        card3 = Card('SPADE', 7)

        cards_list = [card1, card2, card3]

        case1 = self.assert_equals(cards_list, joker_card, True)

        # 2 jokers
        card4 = Card('DIAMONDS', 9)
        card5 = JokerCard()
        card6 = Card('SPADE', 'Q')

        cards_list2 = [card4, card5, card6]

        case2 = self.assert_equals(cards_list2, joker_card, True)

        card7 = Card('HEARTS', 'Q')
        card8 = JokerCard()
        card9 = Card('CLOVER', 9)

        cards_list3 = [card7, card8, card9]

        case3 = self.assert_equals(cards_list3, joker_card, True)

        if not case1 or not case2 or not case3:
            print "------------------ sequence_with_joker failed!"
            print case1, case2, case3
        else:
            print "sequence_with_joker succeeded!"

    def all_jokers(self):
        joker_card = Card('HEARTS', 10)

        card1 = JokerCard()
        card2 = Card('HEARTS', 10)
        card3 = JokerCard()

        cards_list = [card1, card2, card3]

        case1 = self.assert_equals(cards_list, joker_card, True)

        if not case1:
            print "------------------ all_jokers failed!"
        else:
            print "all_jokers succeeded!"
