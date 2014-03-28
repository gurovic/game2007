import socket
import pickle
from hanabi_server import *

PLAYERS_COUNT = 2
PORT = 2008
END_SYMBOL = bytes('abacaba', encoding="utf-8")

def server_start(players_count, port):
    sock = socket.socket()
    sock.bind( ("", port) )
    sock.listen(players_count)
    connections = []
    list_of_players = []
    while len(connections) != PLAYERS_COUNT:
        connections.append(list(sock.accept()))
        print("someone is connected")
    for player in connections:
        data = player[0].recv(20)
        name = data.decode("utf-8")
        player[0].send(pickle.dumps('Start') + END_SYMBOL)
        list_of_players.append(name)
    names = ' '.join(list_of_players)
    for player in connections:    
        player[0].send(pickle.dumps(names) + END_SYMBOL)
    return connections, list_of_players, sock


def engine(connections, players):
    position = init_game()
    while True:
        for i in range(len(connections)):
            connected_pl = connections[i]
            for j in range(len(connections)):
                connection = connections[j]
                connection[0].send(pickle.dumps(['Position', position_for_player(j, position)]) + END_SYMBOL)
            connected_pl[0].send(pickle.dumps(["Your turn"]) + END_SYMBOL)
            data = pickle.loads(connected_pl[0].recv(50))
            make_move(position, data, i)
            if game_result(position) is not None:
                for connection in connections:
                    connection[0].send(pickle.dumps(['Game over ', game_result(position)]) + END_SYMBOL)
                return
 
       
        
connections, players, sock = server_start(PLAYERS_COUNT, PORT)
engine(connections, players)

