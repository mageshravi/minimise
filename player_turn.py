from minimise.game import *
from minimise.card import *
from bson.objectid import ObjectId

game_id = ObjectId("56e4dfe039e5d12dc0d07cda")
player_name = "Nithya"

# get game
game_dict = GameService.find(game_id)
player_hand = GameManager.get_hand_for(game_id, player_name)
joker_card = Card(game_dict['joker_card']['symbol'], game_dict['joker_card']['label'])

laid_cards = []
laid_cards.append(Card("SPADE","Q"))

try:
    GameManager.are_cards_in_hand(player_hand, laid_cards)
except RuntimeError as err:
    print "RuntimeError: %s" % err
    exit()

if GameManager.validate_lay(laid_cards, joker_card):
    # remove cards from hand, save changes to DB
    [player_hand.remove(card_in_hand) \
        for card in laid_cards for card_in_hand in player_hand \
        if card.symbol == card_in_hand.symbol and card.label == card_in_hand.label]

    for card_in_hand in player_hand:
        print card_in_hand.__unicode__()

# player picks card
# save changes to databases
