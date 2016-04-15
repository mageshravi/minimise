import random

__all__ = [
	'Game',
	'GameManager',
	'GameService'
]

from card import *


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

		GameManager.save(self)
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
			GameService.save_player_hand(self.game_id, player_name, hand)
			self.hand[player_name] = hand

		if self.opener is None:
			self.opener = 0
		else:
			self.opener += 1

		self.active_turn = self.opener
		self.open_cards.append(self.deck.pop())

		# save to DB
		GameManager.save(self)


class GameManager():

	@staticmethod
	def save(game):
		if not isinstance(game, Game):
			raise TypeError("game is not an instance of Game")

		# TODO convert objects to dictionaries

		# GameService.save(game)

	@staticmethod
	def get_hand_for(game_id, player_name):
		"""
		Returns cards in hand for player
		returns: list of cards (objects)
		"""
		player_hand_dict = GameService.get_hand_for(game_id, player_name)
		player_hand = []
		for card_dict in player_hand_dict:
			if card_dict['symbol'] == 'JOKER':
				card = JokerCard()
			else:
				card = Card(card_dict['symbol'], card_dict['label'])
			player_hand.append(card)
		return player_hand

	@staticmethod
	def are_cards_in_hand(player_hand, cards_list):
		"""
		Validates if cards in list exist in player's hand
		returns: True
		raises: RuntimeError Card not in player's hand
		"""
		for card in cards_list:
			if any(card_in_hand.symbol == card.symbol \
				and card_in_hand.value == card.value \
				for card_in_hand in player_hand):
				continue
			else:
				raise RuntimeError("Card not in player's hand")
		return True

	@classmethod
	def validate_lay(cls, cards_list, joker_card):
		"""
		Validates if the given list of cards can be laid together
		returns: boolean
		"""
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


from pymongo import MongoClient


class GameService():

	client = MongoClient()
	db = client.minimize_db

	@classmethod
	def find(cls, game_id):
		games_collection = cls.db.games
		games = games_collection.find({'_id': game_id})
		if games.count() == 0:
			raise RuntimeError("Game not found")
		return games[0]

	@classmethod
	def save(cls, game):
        if not isinstance(game, dict):
            raise TypeError("game must be a dictionary")
		games_collection = cls.db.games
		if game.game_id is None:
			game.game_id = games_collection.insert_one(game).inserted_id
		else:
			games_collection.update_one({'_id': game.game_id}, {'$set': game})

	@staticmethod
	def save_player_hand(game_id, player_name, hand):
		players_collection = GameService.db.players

		# primary key
		pk = {
			'name': player_name,
			'game_id':  game_id
		}

		# row a.k.a record
		player = {
			'name': player_name,
			'game_id':  game_id
		}

		# convert list of objects to list of dictionaries
		cards_list = []
		for card in hand:
			cards_list.append(card.__dict__)
		player['hand'] = cards_list

		# find by pk, then insert or update
		if players_collection.find(pk).count() > 0:
			players_collection.update_one(pk, {'$set': player})
		else:
			players_collection.insert_one(player)

	@classmethod
	def get_hand_for(cls, game_id, player_name):
		"""
		Returns cards in hand for player
		returns: list of cards (dictionaries)
		"""
		players_collection = cls.db.players

		players = players_collection.find({'name': player_name, 'game_id': game_id})
		if players.count() == 0:
			return None
		else:
			return players[0]['hand']

	@classmethod
	def display_player_hand(cls, game_id, player_name):
		players_collection = cls.db.players

		print "Player: %s" %(player_name)

		for player in players_collection.find({'name': player_name, 'game_id': game_id}):
			for card in player['hand']:
				if card['symbol'] == 'JOKER':
					print "JOKER"
				else:
					print "%s %s" %(card['label'], card['symbol'])
