from pymongo import MongoClient
import random


class Game(object):

    game_dict = {}

    def __init__(self, players):

        if not isinstance(players, list) and not isinstance(players, tuple):
            raise TypeError("Expecting list/tuple of players")
            # ---------- end if ----------

        self.game_dict = {
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
        self.game_dict['players'] = players

        no_of_packs = len(players) / 5
        if no_of_packs % 5 != 0:
            no_of_packs += 1
        self.game_dict['no_of_packs'] = no_of_packs
        print "No. of packs: %d" % (no_of_packs)

        GameManager.save(self.game_dict)
        print "Game ID: %s" % (str(self.game_dict['game_id']))

    def get_id(self):
        return self.game_dict['game_id']

    def get_players(self):
        return self.game_dict['players']

    def get_no_of_packs(self):
        return self.game_dict['no_of_packs']

    def get_deck(self):
        return self.game_dict['deck']

    def table(self):
        return self.game_dict['table']

    def get_joker_card(self):
        return self.game_dict['joker_card']

    def get_open_cards(self):
        return self.game_dict['open_cards']

    def get_opener(self):
        return self.game_dict['opener']

    def get_active_turn(self):
        return self.game_dict['active_turn']

    def reset_deck(self):
        self.game_dict['deck'] = self.game_dict['table']
        random.shuffle(self.game_dict['deck'])

    def new_round(self):
        from card import PackFactory
        import random

        # prepare deck
        self.game_dict['deck'] = []
        for pack in range(1, self.game_dict['no_of_packs'] + 1):
            self.game_dict['deck'] += PackFactory.create()  # end of for loop

        print "No. of cards in deck %d" % (len(self.game_dict['deck']))

        # shuffle cards in deck
        random.shuffle(self.game_dict['deck'])

        # draw joker for current round
        joker_card = self.game_dict['deck'].pop()
        while joker_card['symbol'] == 'JOKER':
            # put back the joker_card, shuffle
            self.game_dict['deck'].append(joker_card)
            random.shuffle(self.game_dict['deck'])
            # draw new joker card
            joker_card = self.game_dict['deck'].pop()
            # ---------- end while ----------

        # finalise joker card
        self.game_dict['joker_card'] = joker_card

        self.game_dict['hand'] = {}
        for player_name in self.game_dict['players']:
            hand = []
            for i in range(1, 6):
                card = self.game_dict['deck'].pop()
                hand.append(card)
                GameService.save_player_hand(
                    player_name, 
                    hand, 
                    self.game_dict['game_id']
                )
                # ---------- end for ----------

            self.game_dict['hand']['player_name'] = hand

        if self.game_dict['opener'] is None:
            self.game_dict['opener'] = 0
        else:
            self.game_dict['opener'] += 1

        self.game_dict['active_turn'] = self.game_dict['opener']
        self.game_dict['open_cards'].append(self.game_dict['deck'].pop())

        # save to DB
        GameManager.save(self.game_dict)

    def get_hand_for(self, player_name):
        """
        Returns cards in hand for player
        returns: list
        """
        return GameService.get_hand_for(player_name, self.game_id)


class GameFactory():

    @staticmethod
    def create(players):
        return Game(players)

    
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
        return GameService.get_hand_for(player_name, game_id)

    @staticmethod
    def are_cards_in_hand(player_hand, cards_list):
        """
        Validates if cards in list exist in player's hand

        returns: True
        raises: RuntimeError otherwise
        """
        for card in cards_list:
            if any(card_in_hand['symbol'] == card['symbol'] and
                   card_in_hand['value'] == card['value']
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
            # endif

            # get the joker count
            joker_count = cls.remove_jokers(cards_list, joker_card)

            # in sequence?
            if cls.cards_are_sequence(cards_list, joker_count):
                return True
            # endif
            return False
        # endif

    @classmethod
    def cards_are_sequence(cls, cards_list, joker_count):
        """
        Validates if cards are in sequence
        returns: boolean
        """
        if (len(cards_list) + joker_count) < 3:
            return False

        sorted_cards = sorted(
            cards_list,
            key=lambda card: card['value'],
            reverse=True
        )
        prev_card = None
        total_missing_cards = 0
        for card in sorted_cards:
            if prev_card:
                if card['symbol'] != prev_card['symbol']:
                    # Different symbols. Not in sequence
                    return False
                # endif

                if card['value'] == prev_card['value']:
                    # Duplicate card. Not in sequence
                    return False
                # endif

                missing_cards = prev_card['value'] - card['value'] - 1
                total_missing_cards += missing_cards
            # endif
            prev_card = card
        # endfor
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
            if card['value'] == joker_card['value'] \
               or card['symbol'] == 'JOKER':
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
        returns: boolean
        """
        if len(cards_list) == 0:
            return False
        prev_value = cards_list[0]['value']
        for card in cards_list:
            if prev_value != card['value']:
                return False
        return True


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
        if game['game_id'] is None:
            game['game_id'] = games_collection.insert_one(game).inserted_id
        else:
            games_collection.update_one(
                {'_id': game['game_id']},
                {'$set': game}
            )

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
    def display_player_hand(cls, game_id, player_name):
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
