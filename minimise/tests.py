import unittest
from card import CardFactory, JokerCardFactory
from game import GameManager


class GameManagerTest(unittest.TestCase):

    def test_cardsAreSimilar_withDissimilarCards_forFalse(self):
        # empty set
        cards_list = []
        result = GameManager.cards_are_similar(cards_list)
        self.assertFalse(result)

        # 2 cards [4, 5]
        cards_list = []
        cards_list.append(CardFactory.create('HEARTS', 4))
        cards_list.append(CardFactory.create('HEARTS', 5))
        result = GameManager.cards_are_similar(cards_list)
        self.assertFalse(result)

        # 3 cards [10, 10, joker]
        cards_list = []
        cards_list.append(CardFactory.create('DIAMONDS', 10))
        cards_list.append(CardFactory.create('HEARTS', 10))
        cards_list.append(JokerCardFactory.create())
        result = GameManager.cards_are_similar(cards_list)
        self.assertFalse(result)

        # 4 cards [10, 10, 10, 9]
        cards_list = []
        cards_list.append(CardFactory.create('SPADE', 10))
        cards_list.append(CardFactory.create('HEARTS', 10))
        cards_list.append(CardFactory.create('CLOVER', 10))
        cards_list.append(CardFactory.create('CLOVER', 9))
        result = GameManager.cards_are_similar(cards_list)
        self.assertFalse(result)

    def test_removeJokers_forSuccess(self):
        # 0 jokers
        cards_list = self.get_cards('HEARTS', (2, 5, 7))
        cards_list += self.get_cards('SPADE', (6, 8))
        joker_card = CardFactory.create('DIAMONDS', 'K')
        no_of_jokers = GameManager.remove_jokers(cards_list, joker_card)
        self.assertEquals(no_of_jokers, 0)

        # 1 joker
        cards_list = self.get_cards('CLOVER', ('K', 2, 3))
        cards_list += self.get_cards('SPADE', (2, 3))
        joker_card = CardFactory.create('HEARTS', 'K')
        no_of_jokers = GameManager.remove_jokers(cards_list, joker_card)
        self.assertEquals(no_of_jokers, 1)

        # 2 jokers
        cards_list = self.get_cards('CLOVER', ('K', 2, 3))
        cards_list += self.get_cards('SPADE', (2, 3))
        joker_card = CardFactory.create('HEARTS', 2)
        no_of_jokers = GameManager.remove_jokers(cards_list, joker_card)
        self.assertEquals(no_of_jokers, 2)

        # 3 jokers
        cards_list = self.get_cards('DIAMONDS', (2, 3, 4))
        cards_list.append(CardFactory.create('SPADE', 2))
        cards_list.append(JokerCardFactory.create())
        joker_card = CardFactory.create('HEARTS', 2)
        no_of_jokers = GameManager.remove_jokers(cards_list, joker_card)
        self.assertEquals(no_of_jokers, 3)
        
        # 4 jokers
        cards_list = self.get_cards('HEARTS', 'A')
        cards_list.append(CardFactory.create('SPADE', 'A'))
        cards_list.append(CardFactory.create('CLOVER', 'A'))
        cards_list.append(CardFactory.create('DIAMONDS', 'A'))
        joker_card = CardFactory.create('HEARTS', 'A')
        no_of_jokers = GameManager.remove_jokers(cards_list, joker_card)
        self.assertEquals(no_of_jokers, 4)

        # 5 jokers
        cards_list = self.get_cards('HEARTS', 'A')
        cards_list.append(CardFactory.create('SPADE', 'A'))
        cards_list.append(CardFactory.create('CLOVER', 'A'))
        cards_list.append(CardFactory.create('DIAMONDS', 'A'))
        cards_list.append(JokerCardFactory.create())
        joker_card = CardFactory.create('HEARTS', 'A')
        no_of_jokers = GameManager.remove_jokers(cards_list, joker_card)
        self.assertEquals(no_of_jokers, 5)

    def test_cardsAreSequence_withNoJokers_forFailure(self):

        # 1 card, 0 jokers
        cards_list = self.get_cards('CLOVER', ('A'))
        result = GameManager.cards_are_sequence(cards_list, 0)
        self.assertFalse(result)
        
        # 2 card, 0 jokers
        cards_list = self.get_cards('CLOVER', ('A', 2))
        result = GameManager.cards_are_sequence(cards_list, 0)
        self.assertFalse(result)

        # 3 cards, 0 jokers, same symbol
        cards_list = self.get_cards('DIAMONDS', (10, 'K', 'Q'))
        result = GameManager.cards_are_sequence(cards_list, 0)
        self.assertFalse(result)

        # 3 cards, 0 jokers, different symbols
        cards_list = self.get_cards('DIAMONDS', (10, 'J'))
        cards_list += self.get_cards('HEARTS', ('Q'))
        result = GameManager.cards_are_sequence(cards_list, 0)
        self.assertFalse(result)

        # 4 cards, 0 jokers, same symbol
        cards_list = self.get_cards('HEARTS', ('K', 'Q', 'J', 'A'))
        result = GameManager.cards_are_sequence(cards_list, 0)
        self.assertFalse(result)

        cards_list = self.get_cards('DIAMONDS', (2, 2, 3, 3))
        result = GameManager.cards_are_sequence(cards_list, 0)
        self.assertFalse(result)

        # 4 cards, 0 jokers, different symbols
        cards_list = self.get_cards('SPADE', (10, 'J'))
        cards_list += self.get_cards('CLOVER', ('Q', 'K'))
        result = GameManager.cards_are_sequence(cards_list, 0)
        self.assertFalse(result)

        # 5 cards, 0 jokers
        cards_list = self.get_cards('SPADE', (2, 2, 3, 3, 4))
        result = GameManager.cards_are_sequence(cards_list, 0)
        self.assertFalse(result)

    def test_cardsAreSequence_withNoJokers_forSuccess(self):

        # 3 cards, 0 jokers
        cards_list = self.get_cards('DIAMONDS', ('A', 2, 3))
        result = GameManager.cards_are_sequence(cards_list, 0)
        self.assertTrue(result)

        # 4 cards, 0 jokers
        cards_list = self.get_cards('CLOVER', (4, 5, 6, 7))
        result = GameManager.cards_are_sequence(cards_list, 0)
        self.assertTrue(result)

        # 5 cards, 0 jokers
        cards_list = self.get_cards('SPADE', (9, 10, 'J', 'K', 'Q'))
        result = GameManager.cards_are_sequence(cards_list, 0)
        self.assertTrue(result)

    def test_cardsAreSequence_withJokers_forFailure(self):
        
        # 0 card + 1 joker
        result = GameManager.cards_are_sequence([], 1)
        self.assertFalse(result)

        # 0 card + 2 jokers
        result = GameManager.cards_are_sequence([], 2)
        self.assertFalse(result)

    def test_cardsAreSequence_withJokers_forSuccess(self):
        
        # 2 cards + 1 joker
        cards_list = self.get_cards('HEARTS', (3, 5))
        result = GameManager.cards_are_sequence(cards_list, 1)
        self.assertTrue(result)

        # 2 cards + 2 jokers
        result = GameManager.cards_are_sequence(cards_list, 2)
        self.assertTrue(result)

        # 2 cards + 3 jokers
        result = GameManager.cards_are_sequence(cards_list, 3)

        # 3 cards + 1 joker
        cards_list = self.get_cards('SPADE', (8, 10, 'J'))
        result = GameManager.cards_are_sequence(cards_list, 1)
        self.assertTrue(result)

        # 3 cards + 2 jokers
        result = GameManager.cards_are_sequence(cards_list, 2)
        self.assertTrue(result)

        # 4 cards + 1 joker
        cards_list = self.get_cards('DIAMONDS', (2, 3, 5, 6))
        result = GameManager.cards_are_sequence(cards_list, 1)
        self.assertTrue(result)

    def get_cards(self, symbol, labels):
        cards_list = []
        for label in labels:
            cards_list.append(CardFactory.create(symbol, label))
            # ---------- end for ----------
        return cards_list
        
if __name__ == '__main__':
    unittest.main()
