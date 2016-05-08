import unittest
from card import CardFactory, JokerCardFactory
from game import GameManager


class GameManagerTest(unittest.TestCase):

    def test_cardsAreSimilar_withDissimilarCards_forFalse(self):
        # empty set
        cards_list = []
        self.assert_cardsAreSimilar_forFailure(cards_list)

        # 2 cards [4, 5]
        cards_list = []
        cards_list.append(CardFactory.create('HEARTS', 4))
        cards_list.append(CardFactory.create('HEARTS', 5))
        self.assert_cardsAreSimilar_forFailure(cards_list)

        # 3 cards [10, 10, joker]
        cards_list = []
        cards_list.append(CardFactory.create('DIAMONDS', 10))
        cards_list.append(CardFactory.create('HEARTS', 10))
        cards_list.append(JokerCardFactory.create())
        self.assert_cardsAreSimilar_forFailure(cards_list)

        # 4 cards [10, 10, 10, 9]
        cards_list = []
        cards_list.append(CardFactory.create('SPADE', 10))
        cards_list.append(CardFactory.create('HEARTS', 10))
        cards_list.append(CardFactory.create('CLOVER', 10))
        cards_list.append(CardFactory.create('CLOVER', 9))
        self.assert_cardsAreSimilar_forFailure(cards_list)

        # 5 cards [4, 4, 4, 4, joker]
        cards_list = []
        cards_list.append(CardFactory.create('DIAMONDS', 4))
        cards_list.append(CardFactory.create('HEARTS', 4))
        cards_list.append(CardFactory.create('SPADE', 4))
        cards_list.append(CardFactory.create('CLOVER', 4))
        cards_list.append(JokerCardFactory.create())
        self.assert_cardsAreSimilar_forFailure(cards_list)

    def assert_cardsAreSimilar_forFailure(self, cards_list):
        result = GameManager.cards_are_similar(cards_list)
        self.assertFalse(result)

    def test_cardsAreSimilar_withSimilarCards_forSuccess(self):
        # 1 card
        cards_list = [CardFactory.create('DIAMONDS', 'K')]
        self.assert_cardsAreSimilar_forSuccess(cards_list)

        # 2 cards
        cards_list = []
        cards_list.append(CardFactory.create('DIAMONDS', 'K'))
        cards_list.append(CardFactory.create('SPADE', 'K'))
        self.assert_cardsAreSimilar_forSuccess(cards_list)

        # 3 cards
        cards_list = []
        cards_list.append(CardFactory.create('DIAMONDS', 'K'))
        cards_list.append(CardFactory.create('SPADE', 'K'))
        cards_list.append(CardFactory.create('HEARTS', 'K'))
        self.assert_cardsAreSimilar_forSuccess(cards_list)

        # 4 cards
        cards_list = []
        cards_list.append(CardFactory.create('DIAMONDS', 'K'))
        cards_list.append(CardFactory.create('SPADE', 'K'))
        cards_list.append(CardFactory.create('HEARTS', 'K'))
        cards_list.append(CardFactory.create('CLOVER', 'K'))
        self.assert_cardsAreSimilar_forSuccess(cards_list)

        # 5 cards
        cards_list = []
        cards_list.append(CardFactory.create('DIAMONDS', 'K'))
        cards_list.append(CardFactory.create('SPADE', 'K'))
        cards_list.append(CardFactory.create('HEARTS', 'K'))
        cards_list.append(CardFactory.create('CLOVER', 'K'))
        cards_list.append(CardFactory.create('CLOVER', 'K'))
        self.assert_cardsAreSimilar_forSuccess(cards_list)

    def assert_cardsAreSimilar_forSuccess(self, cards_list):
        result = GameManager.cards_are_similar(cards_list)
        self.assertTrue(result)

    def test_removeJokers_forSuccess(self):
        # 0 jokers
        cards_list = self.get_cards('HEARTS', (2, 5, 7))
        cards_list += self.get_cards('SPADE', (6, 8))
        joker_card = CardFactory.create('DIAMONDS', 'K')
        self.assert_removeJokers_forSuccess(cards_list, joker_card, 0)

        # 1 joker
        cards_list = self.get_cards('CLOVER', ('K', 2, 3))
        cards_list += self.get_cards('SPADE', (2, 3))
        joker_card = CardFactory.create('HEARTS', 'K')
        self.assert_removeJokers_forSuccess(cards_list, joker_card, 1)

        # 2 jokers
        cards_list = self.get_cards('CLOVER', ('K', 2, 3))
        cards_list += self.get_cards('SPADE', (2, 3))
        joker_card = CardFactory.create('HEARTS', 2)
        self.assert_removeJokers_forSuccess(cards_list, joker_card, 2)

        # 3 jokers
        cards_list = self.get_cards('DIAMONDS', (2, 3, 4))
        cards_list.append(CardFactory.create('SPADE', 2))
        cards_list.append(JokerCardFactory.create())
        joker_card = CardFactory.create('HEARTS', 2)
        self.assert_removeJokers_forSuccess(cards_list, joker_card, 3)
        
        # 4 jokers
        cards_list = self.get_cards('HEARTS', 'A')
        cards_list.append(CardFactory.create('SPADE', 'A'))
        cards_list.append(CardFactory.create('CLOVER', 'A'))
        cards_list.append(CardFactory.create('DIAMONDS', 'A'))
        joker_card = CardFactory.create('HEARTS', 'A')
        self.assert_removeJokers_forSuccess(cards_list, joker_card, 4)

        # 5 jokers
        cards_list = self.get_cards('HEARTS', 'A')
        cards_list.append(CardFactory.create('SPADE', 'A'))
        cards_list.append(CardFactory.create('CLOVER', 'A'))
        cards_list.append(CardFactory.create('DIAMONDS', 'A'))
        cards_list.append(JokerCardFactory.create())
        joker_card = CardFactory.create('HEARTS', 'A')
        self.assert_removeJokers_forSuccess(cards_list, joker_card, 5)

    def assert_removeJokers_forSuccess(
            self,
            cards_list,
            joker_card,
            no_of_jokers):
        result = GameManager.remove_jokers(cards_list, joker_card)
        self.assertEquals(no_of_jokers, result)

    def test_cardsAreSequence_withNoJokers_forFailure(self):

        # 1 card, 0 jokers
        cards_list = self.get_cards('CLOVER', ('A'))
        self.assert_cardsAreSequence_forFailure(cards_list, 0)
        
        # 2 card, 0 jokers
        cards_list = self.get_cards('CLOVER', ('A', 2))
        self.assert_cardsAreSequence_forFailure(cards_list, 0)

        # 3 cards, 0 jokers, same symbol
        cards_list = self.get_cards('DIAMONDS', (10, 'K', 'Q'))
        self.assert_cardsAreSequence_forFailure(cards_list, 0)

        # 3 cards, 0 jokers, different symbols
        cards_list = self.get_cards('DIAMONDS', (10, 'J'))
        cards_list += self.get_cards('HEARTS', ('Q'))
        self.assert_cardsAreSequence_forFailure(cards_list, 0)

        # 4 cards, 0 jokers, same symbol
        cards_list = self.get_cards('HEARTS', ('K', 'Q', 'J', 'A'))
        self.assert_cardsAreSequence_forFailure(cards_list, 0)

        cards_list = self.get_cards('DIAMONDS', (2, 2, 3, 3))
        self.assert_cardsAreSequence_forFailure(cards_list, 0)

        # 4 cards, 0 jokers, different symbols
        cards_list = self.get_cards('SPADE', (10, 'J'))
        cards_list += self.get_cards('CLOVER', ('Q', 'K'))
        self.assert_cardsAreSequence_forFailure(cards_list, 0)

        # 5 cards, 0 jokers
        cards_list = self.get_cards('SPADE', (2, 2, 3, 3, 4))
        self.assert_cardsAreSequence_forFailure(cards_list, 0)

    def assert_cardsAreSequence_forFailure(self, cards_list, no_of_jokers):
        result = GameManager.cards_are_sequence(cards_list, no_of_jokers)
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
        self.assert_cardsAreSequence_forFailure([], 1)

        # 0 card + 2 jokers
        self.assert_cardsAreSequence_forFailure([], 2)

    def test_cardsAreSequence_withJokers_forSuccess(self):
        
        # 2 cards + 1 joker
        cards_list = self.get_cards('HEARTS', (3, 5))
        self.assert_cardsAreSequence_forSuccess(cards_list, 1)

        # 2 cards + 2 jokers
        self.assert_cardsAreSequence_forSuccess(cards_list, 2)

        # 2 cards + 3 jokers
        self.assert_cardsAreSequence_forSuccess(cards_list, 3)

        # 3 cards + 1 joker
        cards_list = self.get_cards('SPADE', (8, 10, 'J'))
        self.assert_cardsAreSequence_forSuccess(cards_list, 1)

        # 3 cards + 2 jokers
        self.assert_cardsAreSequence_forSuccess(cards_list, 2)

        # 4 cards + 1 joker
        cards_list = self.get_cards('DIAMONDS', (2, 3, 5, 6))
        self.assert_cardsAreSequence_forSuccess(cards_list, 1)

    def assert_cardsAreSequence_forSuccess(self, cards_list, no_of_jokers):
        result = GameManager.cards_are_sequence(cards_list, no_of_jokers)
        self.assertTrue(result)

    def get_cards(self, symbol, labels):
        cards_list = []
        for label in labels:
            cards_list.append(CardFactory.create(symbol, label))
            # ---------- end for ----------
        return cards_list

    def test_validateLay_withValidCards_forSuccess(self):
        # common joker card
        joker_card = CardFactory.create('HEARTS', 'K')

        # ----- 1 card -----

        # joker card
        cards_list = [joker_card]
        self.assert_validateLay_forSuccess(cards_list, joker_card)
        cards_list = [CardFactory.create('SPADE', 'K')]
        self.assert_validateLay_forSuccess(cards_list, joker_card)

        # non-joker card
        cards_list = [CardFactory.create('DIAMONDS', 10)]
        self.assert_validateLay_forSuccess(cards_list, joker_card)

        # ----- 2 cards -----

        # no jokers, 2 similar cards
        cards_list = []
        cards_list.append(CardFactory.create('SPADE', 2))
        cards_list.append(CardFactory.create('DIAMONDS', 2))
        self.assert_validateLay_forSuccess(cards_list, joker_card)

        # 1 joker, 1 non-joker
        cards_list = self.get_cards('CLOVER', (5, 'K'))
        self.assert_validateLay_forSuccess(cards_list, joker_card)

        # 2 jokers
        cards_list = []
        cards_list.append(CardFactory.create('HEARTS', 'K'))
        cards_list.append(JokerCardFactory.create())
        self.assert_validateLay_forSuccess(cards_list, joker_card)

        joker_card = CardFactory.create('SPADE', 9)

        # ----- 3 cards -----

        # sequence without jokers
        cards_list = self.get_cards('SPADE', (2, 3, 4))
        self.assert_validateLay_forSuccess(cards_list, joker_card)

        # sequence with 1 joker
        cards_list = self.get_cards('HEARTS', ('J', 'Q', 9))
        self.assert_validateLay_forSuccess(cards_list, joker_card)

        # sequence with 2 jokers
        cards_list = []
        cards_list.append(CardFactory.create('CLOVER', 10))
        cards_list.append(JokerCardFactory.create())
        cards_list.append(CardFactory.create('SPADE', 9))
        self.assert_validateLay_forSuccess(cards_list, joker_card)

        # similar cards without jokers
        cards_list = self.get_cards('DIAMONDS', (4, 4, 4))
        self.assert_validateLay_forSuccess(cards_list, joker_card)

        cards_list = []
        cards_list.append(CardFactory.create('HEARTS', 7))
        cards_list.append(CardFactory.create('SPADE', 7))
        cards_list.append(CardFactory.create('CLOVER', 7))
        self.assert_validateLay_forSuccess(cards_list, joker_card)

        # similar cards with 1 joker
        cards_list = []
        cards_list.append(CardFactory.create('HEARTS', 7))
        cards_list.append(CardFactory.create('CLOVER', 7))
        self.assert_validateLay_forSuccess(cards_list, joker_card)

        # ----- 4 cards -----

        # sequence without jokers

        # sequence with 1 joker

        # sequence with 2 jokers

        # sequence with 3 jokers

        # similar cards without jokers
        
        # similar cards with 1 joker

        # similar cards with 2 jokers

    def assert_validateLay_forSuccess(self, cards_list, joker_card):
        result = GameManager.validate_lay(cards_list, joker_card)
        self.assertTrue(result)

if __name__ == '__main__':
    unittest.main()
