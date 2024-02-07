from cliente_tcp import init_tcp_socket, authenticate_user, close_tcp_socket

def end_game(tcp_sock):
    close_tcp_socket(tcp_sock)
    return 0


def main():
    tcp_sock = init_tcp_socket()
    authenficated = False
    is_exitting = False
    while not authenficated and not is_exitting:
        authenficated, is_exitting = authenticate_user(tcp_sock)
        print(authenficated, is_exitting)
        print("estoy saliendo")
        print(authenficated, is_exitting)
        if is_exitting:
            end_game(tcp_sock)

    
if __name__ == "__main__":
    main()