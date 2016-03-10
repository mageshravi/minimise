from pymongo import MongoClient

db = MongoClient().minimize_db

print "No. of games to remove: %d" %(db.games.count())
db.games.remove()
print "Pending games: %d" %(db.games.count())

