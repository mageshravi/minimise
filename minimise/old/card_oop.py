__all__ = [
	'Card',
	'JokerCard',
	'Pack'
]

class Card(object):
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
		self.label = 'JOKER'
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
