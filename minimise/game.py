class GameFactory():

    @staticmethod
    def create(players):
        # new dict
        game = {
            'game_id': None,
            'players': None,
            'no_of_packs': 0,
            'deck': [],
            'hand': {},
            'table': [],
            'joker_card': None,
            'open_cards': [],
            'opener': None,
            'active_turn': None
        }

        # set players
        game['players'] = players

        no_of_packs = len(players) / 5
        if no_of_packs % 5 != 0:
            no_of_packs += 1
        game['no_of_packs'] = no_of_packs
        print "No. of packs: %d" % (no_of_packs)

        GameManager.save(game)
        print "Game ID: %s" % (str(game['game_id']))

        return game

    @staticmethod
    def reset_deck(game):
        game['deck'] = game['table']
        random.shuffle(game['deck'])

    @staticmethod
    def new_round(game):
        # prepare deck
        game['deck'] = []
        for pack in range(1, game['no_of_packs'] + 1):
            game['deck'] += Pack.get()
        print "No. of cards in deck %d" % (len(game['deck']))

        # shuffle cards in deck
        random.shuffle(game['deck'])

        # draw joker for current round
        joker_card = game['deck'].pop()
        while joker_card['symbol'] == 'JOKER':
            # put back the joker_card, shuffle
            game['deck'].append(joker_card)
            random.shuffle(game['deck'])
            # draw new joker card
            joker_card = game['deck'].pop()
        # finalise joker card
        game['joker_card'] = joker_card

        game['hand'] = {}
        for player_name in game['players']:
            hand = []
            for i in range(1,6):
                card = game['deck'].pop()
                hand.append(card)
            GameService.save_player_hand(player_name, hand, game['game_id'])
            game['hand']['player_name'] = hand

        if game['opener'] is None:
            game['opener'] = 0
        else:
            game['opener'] += 1

        game['active_turn'] = game['opener']
        game['open_cards'].append(game['deck'].pop())

        # save to DB
        GameManager.save(game)


class GameManager():

    @staticmethod
    def save(game):
        if not isinstance(game, dict):
            raise TypeError("game is not a dictionary")
        GameService.save(game)

    @staticmethod
    def get_hand_for(player_name, game_id):
        """
        Returns cards in hand for player
        returns: list
        """
        return GameService.get_hand_for(palyer_name, game_id)

    @staticmethod
    def are_cards_in_hand(player_hand, cards_list):
        """
        Validates if cards in list exist in player's hand

        returns: True
        raises: RuntimeError otherwise
        """
        for card in cards_list:
            if any(card_in_hand['symbol'] == card['symbol'] \
                   and card_in_hand['value'] == card['value'] \
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
        Validates if cards are in sequence
        returns: boolean
        """
        sorted_cards = sorted(cards_list, key = lambda card: card['value'], reverse = True)
        prev_card = None
        total_missing_cards = 0
        for card in sorted_cards:
            if prev_card:
                if card['symbol'] != prev_card['symbol']:
                    print "Different symbols. Not in sequence"
                    return False
                missing_cards = prev_card['value'] - card['value'] - 1
                total_missing_cards += missing_cards
            prev_card = card
        return joker_count >= total_missing_cards

    @classmethod
    def remove_jokers(cls, cards_list, joker_card):
        """
        Removes jokers from the cards list
        returns: no. of jokers removed
        """
        joker_count = 0
        cards_to_remove = []
        for card in cards_list:
            if card['value'] == joker_card['value'] or card['symbol'] == 'JOKER':
                joker_count += 1
                # do not remove items from the list being iterated
                # save items to be removed in separate list
                cards_to_remove.append(card)

        # remove from original list
        [cards_list.remove(card) for card in cards_to_remove]
        return joker_count

    @classmethod
    def cards_are_similar(cls, cards_list):
        """
        checks if all the cards in the given list are similar
        """
        no_of_cards = len(cards_list)
        prev_value = cards_list[0]['value']
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
            raise RuntimeError("Game not found!")
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

    @classmethod
    def save_player_hand(cls, player_name, hand, game_id):
        """
        Updates cards in hand for player
        """
        players_collection = cls.db.players
        # query condition
        where = {
            'name': player_name,
            'game_id': game_id,
        }
        # row a.k.a record
        player = {
            'name': player_name,
            'game_id': game_id,
            'hand': hand
        }
        # find by pk, then insert or update
        if players_collection.find(where).count() > 0:
            players_collection.update_one(where, {'$set': player})
        else:
            players_collection.insert_one(player)

    @classmethod
    def get_hand_for(cls, player_name, game_id):
        """
        Get cards in hand for player
        returns: list
        """
        players_collection = cls.db.players
        # query condition
        where = {
            'name': player_name,
            'game_id': game_id,
        }
        players = players_collection.find(where)
        if players.count() == 0:
            return []
        else:
            return players[0]['hand']

    @classmethod
    def display_player_hand(cls, player_name, game_id):
        players_collection = cls.db.players
        print "Player: %s" % (player_name)
        # query condition
        where = {
            'name': player_name,
            'game_id': game_id,
        }
        for player in players_collection.find(where):
            for card in player['hand']:
                print "%s %s" % (card['label'], card['symbol'])
