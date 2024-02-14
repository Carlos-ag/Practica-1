import socket
import pickle
from time import sleep
from api import get_api_data

# Configuración inicial
MIN_PLAYERS = 2
PORT = input("Ingrese el número de puerto para el servidor: ")
try:
    PORT = int(PORT)
except ValueError:
    print("El puerto debe ser un número.")
    exit(1)

# Crear el socket UDP
server_socket = socket.socket(family=socket.AF_INET, type=socket.SOCK_DGRAM)
server_socket.bind(('', PORT))
print(f"Servidor UDP listo y escuchando en el puerto {PORT}.")

# Lista para almacenar las direcciones de los clientes
clients = []
questions = get_api_data()  # Asumiendo que esta función ya está definida
current_question = 0

def send_question_to_all():
    if current_question < len(questions):
        for client in clients:
            question = questions[current_question]
            server_socket.sendto(pickle.dumps(question), client)
    else:
        end_game()

def receive_answers():
    answers_received = 0
    while answers_received < len(clients):
        bytes_rx, client_address = server_socket.recvfrom(1024)
        answer, client_id = pickle.loads(bytes_rx)
        print(f"Respuesta recibida de {client_id}: {answer}")
        # Aquí se verificaría la respuesta y se actualizaría la puntuación
        answers_received += 1
    global current_question
    current_question += 1
    send_question_to_all()

def end_game():
    final_scores = "Resultados del juego: "  # Aquí se calcularían los resultados finales
    for client in clients:
        server_socket.sendto(pickle.dumps(final_scores), client)
    print("Juego terminado.")
    server_socket.close()

# Bucle principal del servidor
while True:
    if len(clients) < MIN_PLAYERS:
        print("Esperando a que se conecten más jugadores...")
        data, address = server_socket.recvfrom(1024)
        if address not in clients:
            clients.append(address)
            server_socket.sendto(pickle.dumps("Conectado al servidor de juego."), address)
        if len(clients) == MIN_PLAYERS:
            send_question_to_all()
    else:
        receive_answers()
