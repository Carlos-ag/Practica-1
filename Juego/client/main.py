import socket
import struct

from cliente_tcp import init_tcp_socket, authenticate_user, close_tcp_socket

def end_game(tcp_sock):
    close_tcp_socket(tcp_sock)
    return 0

def join_multicast_group(multicast_group_ip, multicast_port):
    """
    Joins a multicast group to receive messages.
    """

    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM, socket.IPPROTO_UDP)
    sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    
    # Bind to the server address    
    sock.bind(('', multicast_port))
    group = socket.inet_aton(multicast_group_ip)
    mreq = struct.pack('4sL', group, socket.INADDR_ANY)
    sock.setsockopt(socket.IPPROTO_IP, socket.IP_ADD_MEMBERSHIP, mreq)

    

    print("Joined multicast group. Waiting for game data...")
    while True:
        data, _ = sock.recvfrom(1024)
        if data == "GAME STARTS":
            print("Game starts!")
        else:
            print(data.decode())
        
        # Implement game-specific logic based on received data here

def start_game(tcp_sock):
    """
    Waits for multicast group details from the server and then joins the group.
    """
    # send OK to server
    tcp_sock.sendall("OK".encode())
    print("Waiting for multicast group details from server...")
    
    print("estoy bloqueado aqui")
    data = tcp_sock.recv(1024).decode()
    while data == "":
        data = tcp_sock.recv(1024).decode()
    print(data)
    print("that was the data")
    if data.startswith("MULTICAST_GROUP:"):
        _, multicast_group_ip, multicast_port = data.split(":")
        join_multicast_group(multicast_group_ip, int(multicast_port))
        print("connected yo multicast")
    
    tcp_sock.sendall("OK".encode())

def main():
    tcp_sock = init_tcp_socket()
    authenticated = False
    is_exitting = False
    while not authenticated and not is_exitting:
        authenticated, is_exitting = authenticate_user(tcp_sock)
        if is_exitting:
            end_game(tcp_sock)
        elif authenticated:
            start_game(tcp_sock)

if __name__ == "__main__":
    main()
