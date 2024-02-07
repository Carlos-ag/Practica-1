from server_tcp import init_tcp_socket, read_ip_port
from handle_authentification import handle_authentification

def end_game(tcp_sock):
    close_tcp_socket(tcp_sock)
    return 0



def main():
    connection, client_address = init_tcp_socket()
    try:
        user = handle_authentification(connection)
    except:
        print("The user disconnected")


if __name__ == "__main__":
    main()