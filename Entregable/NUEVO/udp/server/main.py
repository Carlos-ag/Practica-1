import socket
import pickle
from api import get_api_data  # Assuming get_api_data is defined correctly

MIN_PLAYERS = 2  # Minimum number of players to start the game

def main():
    try:
        port = int(input("Provide port number (e.g. 6789): "))
    except ValueError:
        print("It has to be a number (e.g. 6789)")
        return

    server_socket = socket.socket(family=socket.AF_INET, type=socket.SOCK_DGRAM)
    server_address = ("127.0.0.1", port)
    server_socket.bind(server_address)
    print("UDP server up and listening")

    players = {}  # Dictionary to maintain the state of players
    questions = get_api_data()  # Obtain questions from the API

    try:
        while True:
            bytes_rx, client_address = server_socket.recvfrom(1024)
            message = pickle.loads(bytes_rx)
            client_id, client_message = message.get('client_id'), message.get('message')

            if client_message == "START":
                players[client_address] = {"id": client_id, "score": 0}
                print(f"Player {client_id} connected. Total players: {len(players)}")

                if len(players) >= MIN_PLAYERS:
                    start_message = {"action": "start", "message": "Game starting!"}
                    for address in players:
                        server_socket.sendto(pickle.dumps(start_message), address)

                    # Assuming all questions are sent at once for simplicity
                    for question in questions:
                        for address in players:
                            server_socket.sendto(pickle.dumps(question), address)

                        for _ in range(len(players)):
                            bytes_rx, answer_address = server_socket.recvfrom(1024)
                            client_response = pickle.loads(bytes_rx)
                            # Check if the message is an answer
                            if 'respuesta' in client_response:
                                correct_answer = question['respuesta_correcta']
                                if client_response['respuesta'] == correct_answer:
                                    players[answer_address]['score'] += 1
                                    result_message = {"message": "Correct! Your score is now " + str(players[answer_address]['score'])}
                                else:
                                    result_message = {"message": "Wrong! Your score remains " + str(players[answer_address]['score'])}
                                server_socket.sendto(pickle.dumps(result_message), answer_address)

            elif client_message == "EXIT":
                if client_address in players:
                    del players[client_address]
                    goodbye_message = {"message": f"Player {client_id} has left the game."}
                    server_socket.sendto(pickle.dumps(goodbye_message), client_address)
                    print(goodbye_message['message'] + f" Total players: {len(players)}")

    except Exception as e:
        print(f"An error occurred: {e}")
    finally:
        server_socket.close()
        print("Server shut down.")

if __name__ == "__main__":
    main()
