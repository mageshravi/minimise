from minimise import Card, JokerCard, GameManager

def assert_validate_lay(cards_list, joker_card, expected_op):
    actual_op = GameManager.validate_lay(cards_list, joker_card)
    return actual_op == expected_op

def three_cards_failure():
    joker_card = Card('HEARTS', 10)
    # two cards
    card1 = Card('SPADE', 5)
    card2 = Card('CLOVER', 10)
    card3 = Card('HEARTS',8)

    cards_list = [card1, card2, card3]

    case1 = assert_validate_lay(cards_list, joker_card, False)

    if not case1:
        print "three_cards_failure failed!"
    else:
        print "three_cards_failure succeeded!"

def three_cards_triplet():
    joker_card = Card('HEARTS', 10)
    # two cards
    card1 = Card('SPADE', 5)
    card2 = Card('CLOVER', 5)
    card3 = Card('HEARTS',5)

    cards_list = [card1, card2, card3]

    case2 = assert_validate_lay(cards_list, joker_card, True)

    if not case2:
        print "three_cards_triplet failed!"
    else:
        print "three_cards_triplet succeeded!"

def three_cards_sequence_without_joker():
    joker_card = Card('HEARTS', 9)

    card1 = Card('SPADE', 5)
    card2 = Card('SPADE', 6)
    card3 = Card('SPADE', 7)

    cards_list = [card1, card2, card3]

    case1 = assert_validate_lay(cards_list, joker_card, True)

    card1 = Card('SPADE', 10)
    card2 = Card('SPADE', 'J')
    card3 = Card('SPADE', 'Q')

    cards_list = [card1, card2, card3]

    case2 = assert_validate_lay(cards_list, joker_card, True)

    if not case1 or not case2:
        print "three_cards_sequence_without_joker failed!"
        print case1, case2
    else:
        print "three_cards_sequence_without_joker succeeded!"

def three_cards_sequence_with_joker():
    joker_card = Card('HEARTS', 9)

    card1 = Card('SPADE', 5)
    card2 = Card('HEARTS', 9)
    card3 = Card('SPADE', 7)

    cards_list = [card1, card2, card3]

    case1 = assert_validate_lay(cards_list, joker_card, True)

    card1 = Card('HEARTS', 9)
    card2 = JokerCard()
    card3 = Card('SPADE', 'Q')

    cards_list = [card1, card2, card3]

    case2 = assert_validate_lay(cards_list, joker_card, True)

    card1 = Card('HEARTS', 'Q')
    card2 = JokerCard()
    card3 = Card('CLOVER', 9)

    cards_list = [card1, card2, card3]


    case3 = assert_validate_lay(cards_list, joker_card, True)

    if not case1 or not case2 or not case3:
        print "three_cards_sequence_without_joker failed!"
        print case1, case2, case3
    else:
        print "three_cards_sequence_without_joker succeeded!"

def three_cards_sequence_failure():
    joker_card = Card('HEARTS', 10)

    card1 = Card('SPADE', 5)
    card2 = Card('HEARTS', 10)
    card3 = Card('SPADE', 9)

    cards_list = [card1, card2, card3]

    actual_op = GameManager.validate_lay(cards_list, joker_card)
    expected_op = False

    case1 = (actual_op == expected_op)

    if not case1:
        print "three_cards_sequence_failure failed!"
    else:
        print "three_cards_sequence_failure succeeded!"

def three_cards_only_joker():
    joker_card = Card('HEARTS', 10)

    card1 = JokerCard()
    card2 = Card('HEARTS', 10)
    card3 = JokerCard()

    cards_list = [card1, card2, card3]

    case1 = assert_validate_lay(cards_list, joker_card, True)

    if not case1:
        print "three_cards_only_joker failed!"
    else:
        print "three_cards_only_joker succeeded!"

def four_cards_quadruplet():
    joker_card = Card('HEARTS', 10)
    # two cards
    card1 = Card('SPADE', 5)
    card2 = Card('CLOVER', 5)
    card3 = Card('HEARTS',5)
    card4 = Card('HEARTS',5)

    cards_list = [card1, card2, card3,card4]

    case1 = assert_validate_lay(cards_list, joker_card, True)

    if not case1:
        print "four_cards_quadruplet failed!"
    else:
        print "four_cards_quadruplet succeeded!"

def four_cards_sequence_without_joker():
    joker_card = Card('HEARTS', 9)

    card1 = Card('SPADE', 5)
    card2 = Card('SPADE', 6)
    card3 = Card('SPADE', 7)
    card4 = Card('SPADE', 8)

    cards_list = [card1, card2, card3, card4]

    case1 = assert_validate_lay(cards_list, joker_card, True)

    card1 = Card('SPADE', 10)
    card2 = Card('SPADE', 'J')
    card3 = Card('SPADE', 'Q')
    card4 = Card('SPADE', 'K')

    cards_list = [card1, card2, card3,card4]

    case2 = assert_validate_lay(cards_list, joker_card, True)

    if not case1 or not case2:
        print "four_cards_sequence_without_joker failed!"
        print case1, case2
    else:
        print "four_cards_sequence_without_joker succeeded!"

def four_cards_sequence_with_joker():
    joker_card = Card('HEARTS', 9)

    # 1 joker card
    card1 = Card('SPADE', 5)
    card2 = Card('SPADE', 7)
    card3 = Card('SPADE', 8)
    card4 = Card('SPADE', 9)

    cards_list = [card1, card2, card3, card4]

    case1 = assert_validate_lay(cards_list, joker_card, True)

    # 2 joker cards
    card1 = Card('CLOVER', 9)
    card2 = Card('SPADE', 'Q')
    card3 = Card('SPADE', 'K')
    card4 = JokerCard()

    cards_list = [card1, card2, card3,card4]

    case2 = assert_validate_lay(cards_list, joker_card, True)

    # 2 joker cards
    card4 = Card('HEARTS', 'J')
    card1 = Card('HEARTS', 'Q')
    card2 = JokerCard()
    card3 = Card('CLOVER', 9)

    cards_list = [card1, card2, card3, card4]

    case3 = assert_validate_lay(cards_list, joker_card, True)

    if not case1 or not case2 or not case3:
        print "four_cards_sequence_with_joker failed!"
        print case1, case2, case3, card4
    else:
        print "four_cards_sequence_with_joker succeeded!"

def four_cards_only_joker():
    joker_card = Card('HEARTS', 10)

    card1 = JokerCard()
    card2 = Card('HEARTS', 10)
    card3 = JokerCard()
    card4 = Card('HEARTS', 10)

    cards_list = [card1, card2, card3, card4]

    case1 = assert_validate_lay(cards_list, joker_card, True)

    if not case1:
        print "four_cards_only_joker failed!"
    else:
        print "four_cards_only_joker succeeded!"

def four_cards_failure():
    joker_card = Card('HEARTS', 10)

    card1 = Card('SPADE', 5)
    card2 = Card('CLOVER', 10)
    card3 = Card('HEARTS',8)
    card4 = Card('HEARTS',8)

    cards_list = [card1, card2, card3, card4]

    case1 = assert_validate_lay(cards_list, joker_card, False)

    if not case1:
        print "four_cards_failure failed!"
    else:
        print "four_cards_failure succeeded!"

three_cards_failure()
three_cards_triplet()
three_cards_sequence_without_joker()
three_cards_sequence_failure()
three_cards_only_joker()

four_cards_quadruplet()
four_cards_sequence_without_joker()
four_cards_only_joker()
four_cards_failure()
