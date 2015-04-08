def finish_game(game_result):
    if game_result:
        print('You win')
    elif game_result is False:
        print('You lose')

def is_int(el):
    try:
        int(el)
        return True
    except:
        return False

def move(client_position, players, player_num):
    commands = ["put", "discard", "support"]
    print("YOUR TURN:")
    if len(client_position.players_hands[player_num]):
        print('  put [card_number]')
        print('  discard [card_number]')
    if client_position.hints_count:
        print("  support [player's number] [color or value]\n  or    support [color or value] (next player)")
    ready = 0
    my_cards_quantity = len(client_position.players_hands[player_num])
    while ready == 0:
        ready = 1
        client_step = input().split()
        if (    client_step[0] == 'support'
            and len(client_step) in [2, 3]
            and is_int(client_step[1])
            and client_step[1] < len(players)
            and int(client_step[2]) in range(1, 6) if is_int(client_step[2]) else
                client_step[2].lower() in ["blue", "green", "red", "yellow", "white"]    ):
            if client_step[1] == player_num:
                ready = 0
                print("You can't help yourself.")
            elif len(client_step) == 3:
                move = ['support', int(client_step[1]), client_step[2]]
            else:
                move = ['support', players[(playes_num + 1) % len(players)], int(client_step[1])]
        elif (    client_step[0] == 'discard'
              and len(client_step) == 2
              and is_int(client_step[1])
              and int(client_step[1]) in range(my_cards_quantity)):
            move = ['discard', int(client_step[1])]
        elif (    client_step[0] == 'put'
              and len(client_step) == 2
              and is_int(client_step[1])
              and int(client_step[1]) in range(my_cards_quantity)):
            move = ['put', int(client_step[1])]
        else:
            print("Incorrect turn.")
            ready = 0
    return move

    

def colors_and_cards(cards):
    out = ["Blue:", "Green:", "Red:", "Yellow:", "White:"]
    for card in cards:
        out[card[1]] += " " + str(card[0])
    return out

def print_position(client_position, players, client_player_num):
    print("Lifes:", client_position.lifes_count, end="   ")
    print("Hints:", client_position.hints_count)
    print("Table:")
    print(colors_and_cards(client_position.table))
    print("Cemetery:")
    print(colors_and_cards(client_position.cemetery))
    for player_num in range(len(players)):
        if player_num != client_player_num:
            print(str(player_num) + ':' + players[player_num] + "'s cards:")
            for cards_color in colors_and_cards(client_position.players_hands[player_num]):
                print("--" + cards_color)
            print('WHAT KNOWS THIS PLAYER:')
            for i in range(len(client_position.players_hands[client_player_num])):
                print(i, client_position.players_hands[client_player_num][i].hint)
                 
    print('YOUR CARDS:') 
    for i in range(len(client_position.players_hands[client_player_num])):
        print(i, client_position.players_hands[client_player_num][i].hint)
    print('Last hint:', client_position.hint) 
