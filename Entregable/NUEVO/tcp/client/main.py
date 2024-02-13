import socket
import struct
from cliente_tcp import init_tcp_socket, authenticate_user, close_tcp_socket, end_game


def main():
    """
    Función principal del cliente
    """
    tcp_sock = init_tcp_socket()
    authenticated = False
    is_exitting = False
    while not authenticated and not is_exitting:
        authenticated, is_exitting = authenticate_user(tcp_sock)
        if is_exitting:
            end_game(tcp_sock)
            return 0
    
    tcp_sock.sendall("READY".encode())

    print("Waiting for the server to start the game")

    data = tcp_sock.recv(1024).decode()
    while data != "GAME STARTS":
        data = tcp_sock.recv(1024).decode() 
    print(data)


if __name__ == "__main__":
    main()
