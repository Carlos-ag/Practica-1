import socket
import pickle
from authentification_functions import login_user, register_user, delete_user

class TCPServer:
    def __init__(self, host='localhost', port=8080):
        self.host = host
        self.port = port
        self.server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server_socket.bind((self.host, self.port))
        self.server_socket.listen()

    def handle_client(self, client_socket):
        while True:
            try:
                data = client_socket.recv(1024)
                if not data:
                    break
                request = pickle.loads(data)
                if request['action'] == 'login':
                    response = login_user(request['user'], request['password'])
                elif request['action'] == 'register':
                    response = register_user(request['user'], request['password'])
                elif request['action'] == 'delete':
                    response = delete_user(request['user'], request['password'])
                else:
                    response = {'status': 'error', 'message': 'Invalid action'}

                client_socket.send(pickle.dumps(response))
            except Exception as e:
                print(f"Error: {e}")
                break
        client_socket.close()

    def run(self):
        print(f"Server listening on {self.host}:{self.port}")
        while True:
            client_socket, _ = self.server_socket.accept()
            print("Connection established")
            self.handle_client(client_socket)

if __name__ == '__main__':
    server = TCPServer()
    server.run()
