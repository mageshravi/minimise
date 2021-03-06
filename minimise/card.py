class CardFactory():
    valid_symbols = ('SPADE', 'CLOVER', 'HEARTS', 'DIAMONDS')
    valid_labels = ('A', 2, 3, 4, 5, 6, 7, 8, 9, 10, 'J', 'Q', 'K')
    spl_values = {
	'A': 1,
	'J': 11,
	'Q': 12,
	'K': 13
    }

    @staticmethod
    def create(symbol, value):
        
        # validate symbol and value
        if symbol not in self.valid_symbols:
            raise TypeError("Not a valid symbol")
        if label not in self.valid_labels:
	    raise ValueError("Invalid label: %s" %(label))

        value = label
        if label in ('A', 'J', 'Q', 'K'):
            value = self.spl_values[label]

        card = {
            'symbol': symbol,
            'label': label,
            'value': value
        }

        return card


class JokerCardFactory():

    @staticmethod
    def create():
        return {
            'symbol': 'JOKER',
            'label': 'JOKER',
            'value': 0
        }


class PackFactory():

    @staticmethod
    def create():
        list_cards = []
        for symbol in Card.valid_symbols:
            for label in Card.valid_labels:
                list_cards.append(CardFactory.create(symbol, value))

        # add two joker cards
        list_cards += [JokerCardFactory.create(), JokerCardFactory.create()]
        return list_cards
