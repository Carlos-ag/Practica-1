import socket
import threading
from server_tcp import read_ip_port, handle_client_connection, init_tcp_socket
from handle_authentification import handle_authentification



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
