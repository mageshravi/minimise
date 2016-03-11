from minimise import *

# start game
players = ('Nithya', 'Magesh', 'Susi', 'Raj', 'Varun', 'Kamal', 'Giri')
game = Game(players)
game.new_round()

# get cards for each player
# for player_name in players:
# 	print GameService.display_player_hand(game.game_id, player_name)

print "Joker card: %s" % (game.joker_card.__unicode__())
print "Open card: %s" % (game.open_cards[0].__unicode__())
print "Opener: %s" %(game.players[game.opener])
print "No. of cards in deck: %d" %(len(game.deck))

print "%s's cards:" % (game.players[game.opener])
GameService.display_player_hand(game.game_id, game.players[game.opener])
