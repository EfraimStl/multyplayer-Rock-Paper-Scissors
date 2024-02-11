import socket
from _thread import *
import pickle
from game import Game
import constants

server = constants.SERVER
port = constants.PORT

server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

try:
    server_socket.bind((server, port))
except socket.error as e:
    str(e)

server_socket.listen(2)
print("Server is listening...")

connected = set()
games = {}
id_count = 0


def threaded_client(client_socket, player, game_id):
    global id_count
    client_socket.send(str.encode(str(player)))

    while True:
        try:
            data = client_socket.recv(4096).decode()

            if game_id in games:
                game = games[game_id]

                if not data:
                    print("Disconnected")
                    break
                else:
                    if data == "reset":
                        game.reset_moves()
                    elif data == "quit":
                        game.reset()
                    elif data != "get":
                        game.play(player, data)

                        if game.both_went():
                            winner = game.winner()
                            if winner == 0 or winner == 1:
                                game.wins[winner] += 1
                            else:
                                game.ties += 1

                reply = game
                client_socket.sendall(pickle.dumps(reply))
            else:
                break
        except:
            break

    print("Lost connection")
    try:
        games.pop(game_id)
        print("Closing game", game_id)
    except:
        pass

    id_count -= 1
    client_socket.close()



while True:
    client_socket, client_address = server_socket.accept()
    print(f"Connected to  {client_address}")

    id_count += 1

    p = 0
    game_id = (id_count - 1) // 2
    if id_count % 2 == 1:
        games[game_id] = Game(game_id)
        print("Creating a new game...")
    else:
        games[game_id].ready = True
        p = 1

    start_new_thread(threaded_client, (client_socket, p, game_id))


