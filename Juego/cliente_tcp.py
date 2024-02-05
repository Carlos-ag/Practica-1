import socket
import pickle

class TCPClient:
    def __init__(self, server_host='localhost', server_port=8080):
        self.server_host = server_host
        self.server_port = server_port
        self.client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.client_socket.connect((self.server_host, self.server_port))

    def send_request(self, request):
        self.client_socket.send(pickle.dumps(request))
        response = self.client_socket.recv(1024)
        return pickle.loads(response)

    def close(self):
        self.client_socket.close()

if __name__ == '__main__':
    client = TCPClient()
    # Ejemplo de solicitud de registro
    response = client.send_request({'action': 'register', 'user': 'username', 'password': 'password'})
    print(response)
    # Asegúrate de cerrar la conexión cuando hayas terminado
    client.close()
