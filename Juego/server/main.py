import socket
import threading
from server_tcp import read_ip_port, init_tcp_socket
import struct
from handle_authentification import handle_authentification
import time
from api import get_api_data

# Shared structure for authenticated users with a threading lock for thread-safe access
authenticated_users = []
users_lock = threading.Lock()
global MIN_PLAYERS
MIN_PLAYERS = 1
multicast_group_ip = '224.1.1.1'
multicast_port = 5008
global questions
questions = get_api_data()
global game_started
game_started = False


def handle_client_connection(client_socket):
    global min_players
    global game_started
    try:
        username, connection_user = handle_authentification(client_socket)
        user = {
            "username": username,
            "connection_tcp": connection_user,
            "score": 0,
        }
        if user:  # Assuming handle_authentification returns a user object on success
            with users_lock:  # Ensure thread-safe modification of the authenticated_users list
                authenticated_users.append(user)
                # recv OK from client
                print("Waiting for OK from client")
                print(client_socket.recv(1024).decode())
                print("OK received")
                if (len(authenticated_users) >= MIN_PLAYERS) and not game_started:
                    game_started = True
                    start_multicast()

                   
                    
    except Exception as e:
        print("Error during client handling: ", e)
    finally:
        client_socket.close()

def send_multicast_message(message):
    sock.sendto(message.encode(), (multicast_group_ip, multicast_port)) 

def start_udp_socket():
    """
    Starts a UDP socket to send messages to all connected clients.
    """
    # you have to stablish a connection with all the authenticated_users
    # so you will have to send them a 
    

def compute_score(time_to_answer):
    return 10 * (1 - time_to_answer / 20)


def start_questions_game(questions, authenticated_users):
    # you will have to use threading to send the questions to all the users
    # for each user stablish connection using a new UDP socket
    # send the question to the user
    # wait for the answer or a timeout of 20 seconds
    # if the user answers correctly, GOOD ANSWER your new score is X
    # if the user answers incorrectly, BAD ANSWER the correct answer was X and here is the new score
    return 0



def start_game_multicast(sock):

    # Send data to the multicast group
    sock.sendto("Let's starts the game!".encode(), (multicast_group_ip, multicast_port))
 
    for i in range(5):
        message = f"GAME STARTS IN {5 - i} SECONDS..."
        send_multicast_message(message)
        time.sleep(1)
    
    send_multicast_message("GAME STARTS")

    start_questions_game(questions, authenticated_users)

def start_multicast():
    sock = start_multicast_group()
    send_multicast_to_users()
    start_game_multicast(sock)



def start_multicast_group():
    """
    Starts a multicast group to send messages to all connected clients.
    """

    print("ESTOY EN EL MULTICAST")

    print("EL JUEGO HA EMPEZADO")
    # Create the socket
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

    # Set the time-to-live for messages to 1 so they don't go past the local network segment
    ttl = struct.pack('b', 1)
    sock.setsockopt(socket.IPPROTO_IP, socket.IP_MULTICAST_TTL, ttl)

    return sock

    

 
    


def send_multicast_to_users():
    # Define multicast group IP and port
   
    print("Starting game...")

    # Inform all authenticated users about the multicast group
    info_message = f"MULTICAST_GROUP:{multicast_group_ip}:{multicast_port}"
    print(f"Sending multicast info to {len(authenticated_users)} users...")
    print(authenticated_users)
    print("hola")

    for user in authenticated_users:
        print(user)
        try:
            # Assuming each 'user' object has a reference to its TCP socket
            user_socket = user['connection_tcp']
            print("esto es lo que se va a enviar")
            print(info_message)
            user_socket.sendall(info_message.encode())
            print("enviado")
            # recv OK from client
            print("Waiting for OK from client")
            print(user_socket.recv(1024).decode())
            print("OK received")
            
        except Exception as e:
            print(f"Failed to send multicast info to {user['username']}: {e}")
        
    








def main():
    global game_started
    server_socket = init_tcp_socket()
    print("Server is listening on {}".format(server_socket.getsockname()))

    try:
        while not game_started:
            connection, client_address = server_socket.accept()
            print(f"Connection from {client_address} has been established.")
            client_tcp_thread = threading.Thread(target=handle_client_connection, args=(connection,))
            client_tcp_thread.start() 
        
     
    except KeyboardInterrupt:
        print("Server is shutting down.")
    finally:
        server_socket.close()

if __name__ == "__main__":
    main()
