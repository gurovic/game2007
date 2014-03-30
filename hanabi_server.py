import random
from copy import deepcopy
from settings import PLAYERS_COUNT

BLUE, GREEN, RED, YELLOW, WHITE = 0, 1, 2, 3, 4
color_names = ['blue', 'green', 'red', 'yellow', 'white']

if PLAYERS_COUNT < 4:
    PLAYERS_CARDS = 5
else:
    PLAYERS_CARDS = 4

MAX_HINTS = 8

class Position:
    pass

class Card(list):
    def __init__(self, *args):
        self.hint = ""
        list.__init__(self, *args)


def create_position(players_cards, deck):
    position = Position() 
    position.lifes_count = 3
    position.hints_count = MAX_HINTS
    position.player_number = 0
    position.players_hands = players_cards
    position.cemetery = []
    position.last_stroke = None
    position.cards_on_the_table = 0 
    position.table = []
    position.deck = deck
    position.hint = []
    return position

def colors_and_cards(cards):
    out = ["Blue:", "Green:", "Red:", "Yellow:", "White:"]
    for card in cards:
        out[card[1]] += " " + str(card[0])
    return out

def make_deck():
    cards = [[] for i in range(50)]
    colours = [BLUE, GREEN, RED, YELLOW, WHITE]
    numbers = [1] * 3 + [2] * 2 + [3] * 2 + [4] * 2 + [5]
    k = 0
    for i in range(5):
        for j in range(10):
            cards[k] = Card([numbers[j], colours[i]])
            k += 1
    random.shuffle(cards)
    return cards

def make_move(position, move, player_number):
    player_hand = position.players_hands[player_number]
    if move[0] == 'discard':
        position.cemetery.append(player_hand[move[1]])
        if position.deck:
            player_hand[move[1]] = position.deck.pop()
        else:
            del player_hand[move[1]]
        position.hints_count = min(position.hints_count + 1, MAX_HINTS)
    elif move[0] == 'put':
        if player_hand[move[1]] not in position.table and (player_hand[move[1]][0] == 1 or [player_hand[move[1]][0] - 1, player_hand[move[1]][1]] in position.table): 
            position.cards_on_the_table += 1
            position.table.append(player_hand[move[1]])
        else:
            position.cemetery.append(player_hand[move[1]])
            position.lifes_count -= 1
        if position.deck:
            player_hand[move[1]] = position.deck.pop()
        else:
            del player_hand[move[1]]
        if player_hand[move[1]][0] == 5:
            position.hints_count = min(position.hints_count + 1, MAX_HINTS)
    elif move[0] == 'support':
        position.hints_count -= 1
        hint_player = move[1]
        hint_value = move[2]
        position.hint = [hint_player, hint_value]  # player number, hint
        if hint_value in '12345':
            for card in position.players_hands[hint_player]:
                if card.hint:
                    card.hint += ", "
                if card[0] == int(hint_value):
                    card.hint += hint_value
                else:
                    card.hint += ("NOT " + hint_value)  
        else:
            for card in position.players_hands[hint_player]:
                if card.hint:
                    card.hint += ", "
                if color_names.index(hint_value.lower()) == card[1]:
                    card.hint += hint_value
                else:
                    card.hint += ("NOT " + hint_value)  

def give_cards(cards):
    players_cards = [[] for i in range(PLAYERS_COUNT)]
    for i in range(PLAYERS_COUNT):
        for j in range(PLAYERS_CARDS):
            players_cards[i].append(cards.pop())
            players_cards[i][-1].hint = ""
    return players_cards

def position_for_player(player_number, position):
    position_send = deepcopy(position)
    for card in position_send.players_hands[player_number]:
        card[0] = card[1] = None
    return position_send

def game_result(position):
    if position.cards_on_the_table == 25:
        result = True
    elif position.lifes_count == 0:
        result = False
    else: 
        result = None

    return result


def init_game():
    deck = make_deck()
    player_cards = give_cards(deck)
    position = create_position(player_cards, deck)
    return position
