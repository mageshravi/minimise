from minimise.GameService import *

games_collection = GameService.all()

games = games_collection.find()

for game in games:
    print game['_id']
    for player in game['players']:
        print player
        GameService.display_player_hand(game['_id'], player)
