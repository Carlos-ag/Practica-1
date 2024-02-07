import socket
import struct
from cliente_tcp import init_tcp_socket, authenticate_user, close_tcp_socket, end_game


def main():
    tcp_sock = init_tcp_socket()
    authenticated = False
    is_exitting = False
    while not authenticated and not is_exitting:
        authenticated, is_exitting = authenticate_user(tcp_sock)
        if is_exitting:
            end_game(tcp_sock)
            return 0
    
    # enviar al server que el cliente esta listo
    tcp_sock.sendall("READY".encode())

    # recibir el mensaje de bienvenida
    data = tcp_sock.recv(1024).decode()
    print(data)

if __name__ == "__main__":
    main()
