import socket 
import sys
from handle_authentification import handle_authentification , handle_client_connection
from server_tcp import init_tcp_socket
import os
import threading
import global_variables


def main():
    global_variables.init()

    server_socket = init_tcp_socket()
    print("Server is listening on {}".format(server_socket.getsockname()))

    try:
        while not global_variables.game_started:
            connection, client_address = server_socket.accept()
            print(f"Connection from {client_address} has been established.")
            client_tcp_thread = threading.Thread(target=handle_client_connection, args=(connection,))
            client_tcp_thread.start()

        print("Hola soy el server y el juego ya comenzo")

        # for all the users, receive the OK
        for user in global_variables.authenticated_users:
            try:
                print(user['connection_tcp'].recv(1024).decode())
                user['connection_tcp'].sendall("OK".encode())
            except:
                print("Error al recibir OK")
                continue         
        
     
    except KeyboardInterrupt:
        print("Server is shutting down.")
    finally:
        server_socket.close()

if __name__ == "__main__":
    main()
