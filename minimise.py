import random
import datetime

from pymongo import MongoClient

__all__ = [
	'Card',
	'Pack',
	'Game',
	'GameManager',
	'GameService'
]

class Card():
	valid_symbols = ('SPADE', 'CLOVER', 'HEARTS', 'DIAMONDS')
	valid_labels = ('A', 2, 3, 4, 5, 6, 7, 8, 9, 10, 'J', 'Q', 'K')
	spl_values = {
		'A': 1,
		'J': 11,
		'Q': 12,
		'K': 13
	}
	symbol = None
	label = None
	value = None

	def __init__(self, symbol, label):
		if symbol not in self.valid_symbols:
			raise TypeError("Not a valid symbol")
		if label not in self.valid_labels:
			raise ValueError("Invalid label: %s" %(label))
		self.symbol = symbol
		self.label = label
		if label in ('A', 'J', 'Q', 'K'):
			self.value = self.spl_values[label]
		else:
			self.value = label

	def __unicode__(self):
		return '%s %s' %(self.value, self.symbol)


class JokerCard(Card):

	def __init__(self):
		self.symbol = 'JOKER'
		self.value = 0


class Pack():

	@staticmethod
	def get():
		list_cards = []
		for symbol in Card.valid_symbols:
			for value in Card.valid_labels:
				list_cards.append(Card(symbol, value))
		list_cards += [JokerCard(), JokerCard()]
		return list_cards


class Game():
	game_id = None
	players = None
	no_of_packs = 0
	deck = []
	hand = {}
	table = []
	joker_card = None
	open_cards = []
	opener = None
	active_turn = None

	def __init__(self, players):
		if not isinstance(players, list) and not isinstance(players, tuple):
			raise TypeError("Expecting list/tuple of players!")
		self.players = players

		no_of_packs = len(self.players) / 5
		if no_of_packs % 5 != 0:
			no_of_packs += 1
		self.no_of_packs = no_of_packs
		print "No. of packs: %d" %(no_of_packs)

		game_service = GameService()
		game_service.save(self)
		print "Game ID: %s" % (str(self.game_id))

	def reset_deck(self):
		self.deck = self.table
		random.shuffle(self.deck)

	def new_round(self):
		self.deck = []
		for pack in range(1, self.no_of_packs+1):
			self.deck += Pack.get()
		print "No. of cards in deck: %d" %(len(self.deck))

		random.shuffle(self.deck)

		# draw joker for current round
		joker_card = self.deck.pop()

		while isinstance(joker_card, JokerCard):
			# put back the joker card, shuffle
			self.deck.append(joker_card)
			random.shuffle(self.deck)
			# draw a new joker card
			joker_card = self.deck.pop()

		self.joker_card = joker_card

		for player_name in self.players:
			hand = []
			for i in range(1,6):
				card = self.deck.pop()
				hand.append(card)
			GameService.save_player_hand(self, player_name, hand)
			self.hand[player_name] = hand

		if self.opener is None:
			self.opener = 0
		else:
			self.opener += 1

		self.active_turn = self.opener

		self.open_cards.append(self.deck.pop())


class GameManager():

	@classmethod
	def validate_lay(cls, cards_list, joker_card):
		no_of_cards = len(cards_list)

		if no_of_cards == 0:
			return False
		elif no_of_cards == 1:
			return True
		elif no_of_cards == 2:
			# is duet?
			if cls.cards_are_similar(cards_list):
				return True
			elif cls.remove_jokers(cards_list, joker_card) > 0:
				return True
			return False
		elif no_of_cards < 6:
			# are similar?
			if cls.cards_are_similar(cards_list):
				return True

			# get the joker count
			joker_count = cls.remove_jokers(cards_list, joker_card)

			# in sequence?
			if cls.cards_are_sequence(cards_list, joker_count):
				return True
			return False

	@classmethod
	def cards_are_sequence(cls, cards_list, joker_count):
		"""
		returns True if cards are in sequence. Else False
		"""
		sorted_cards = sorted(cards_list, key = lambda card: card.value, reverse = True)
		prev_card = None
		total_missing_cards = 0
		for card in sorted_cards:
			if prev_card:
				if card.symbol != prev_card.symbol:
					print "Different symbols. Not in sequence"
					return False
				missing_cards = prev_card.value - card.value - 1
				total_missing_cards += missing_cards
			prev_card = card
		return joker_count >= total_missing_cards

	@classmethod
	def remove_jokers(cls, cards_list, joker_card):
		"""
		Removes jokers from the given list and
		returns the no. of jokers removed
		"""
		joker_count = 0
		cards_to_remove = []
		for card in cards_list:
			if card.value == joker_card.value or isinstance(card, JokerCard):
				joker_count += 1
				# do not remove items from the list being iterated
				# save the items to be removed in a separate list
				cards_to_remove.append(card)

		# remove from original list
		for card in cards_to_remove:
			cards_list.remove(card)

		return joker_count

	@classmethod
	def cards_are_similar(cls, cards_list):
		"""
		checks if all the cards in the given list are similar
		i.e., duet, triplet, quadruplet, etc.
		"""
		no_of_cards = len(cards_list)
		prev_value = cards_list[0].value
		for card in cards_list:
			if prev_value != card.value:
				return False
		return True


class GameService():
	client = MongoClient()
	db = client.minimize_db

	@staticmethod
	def save(game):
		if not isinstance(game, Game):
			raise TypeError("game is not an instance of Game")
		games_collection = GameService.db.games
		if game.game_id is None:
			game.game_id = games_collection.insert_one(game.__dict__).inserted_id
		else:
			games_collection.update_one({'_id': game.game_id}, {'$set': game.__dict__})

	@staticmethod
	def save_player_hand(game, player_name, hand):
		players_collection = GameService.db.players

		player = {
			'name': player_name,
			'game_id':  game.game_id
		}
		# convert list of objects to list of dictionaries
		cards_list = []
		for card in hand:
			cards_list.append(card.__dict__)
		player['hand'] = cards_list

		# find by name, then insert or update
		if players_collection.find({'name': player_name}).count() > 0:
			players_collection.update_one({'name': player_name}, {'$set': player})
		else:
			players_collection.insert_one(player)

	@staticmethod
	def get_hand_for(game_id, player_name):
		players_collection = GameService.db.players

		players = players_collection.find({'name': player_name, 'game_id': game_id})
		if players.count() == 0:
			return None
		else:
			return players[0]['hand']

	@staticmethod
	def display_player_hand(game_id, player_name):
		players_collection = GameService.db.players

		print "Player: %s" %(player_name)

		for player in players_collection.find({'name': player_name, 'game_id': game_id}):
			for card in player['hand']:
				if isinstance(card, JokerCard):
					print "JOKER"
				else:
					print "%s %s" %(card['value'], card['symbol'])
