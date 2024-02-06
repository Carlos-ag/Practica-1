from cliente_tcp import init_tcp_socket, authenticate_user, close_tcp_socket


def main():
    sock = init_tcp_socket()
    authenficated = False
    while not authenficated:
        authenficated = authenticate_user(sock)

    # aqui ya sabemos que el usuario esta autenticado

    print("usuario autenticado")
    close_tcp_socket(sock)
    print("socket cerrado")
    


if __name__ == "__main__":
    main()