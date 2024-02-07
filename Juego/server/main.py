import socket
import threading
from server_tcp import read_ip_port, init_tcp_socket
from handle_authentification import handle_authentification

# Shared structure for authenticated users with a threading lock for thread-safe access
authenticated_users = []
users_lock = threading.Lock()
global MIN_PLAYERS
MIN_PLAYERS = 1

def handle_client_connection(client_socket):
    global min_players
    try:
        username, connection_user = handle_authentification(client_socket)
        user = {
            "username": username,
            "connection_tcp": connection_user
        }
        if user:  # Assuming handle_authentification returns a user object on success
            with users_lock:  # Ensure thread-safe modification of the authenticated_users list
                authenticated_users.append(user)
                # recv OK from client
                print("Waiting for OK from client")
                print(client_socket.recv(1024).decode())
                print("OK received")
                if len(authenticated_users) >= MIN_PLAYERS:
                    start_game()  # Start the game when there are at least two authenticated users
    except Exception as e:
        print("Error during client handling: ", e)
    finally:
        client_socket.close()

def start_game():
    # Define multicast group IP and port
    multicast_group_ip = '224.1.1.1'
    multicast_port = 5008
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
        except Exception as e:
            print(f"Failed to send multicast info to {user['username']}: {e}")
    
    # Clear the authenticated_users list after sending the info
    authenticated_users.clear()




def main():
    server_socket = init_tcp_socket()
    print("Server is listening on {}".format(server_socket.getsockname()))

    try:
        while True:
            connection, client_address = server_socket.accept()
            print(f"Connection from {client_address} has been established.")
            client_thread = threading.Thread(target=handle_client_connection, args=(connection,))
            client_thread.start()
    except KeyboardInterrupt:
        print("Server is shutting down.")
    finally:
        server_socket.close()

if __name__ == "__main__":
    main()
