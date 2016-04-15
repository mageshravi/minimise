from minimise.game import *

# start game
players = ('Nithya', 'Magesh', 'Susi', 'Raj', 'Varun', 'Kamal', 'Giri')
game = GameFactory.create(players)
game.new_round()

print "Joker card: %s" % (game.get_joker_card())
print "Open card: %s" % (game.get_open_cards()[0])
print "Opener: %s" % game.get_players()[game.get_opener()]
print "No. of cards in deck: %d" % len(game.get_deck())

print "%s's cards:" % (game.get_players()[game.get_opener()])
GameService.display_player_hand(game.get_id(), game.get_players()[game.get_opener()])
