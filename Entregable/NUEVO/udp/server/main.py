import socket
import pickle
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

# Diccionario para almacenar las direcciones de los clientes y sus puntajes
client_scores = {}
questions = get_api_data() 
current_question = 0

def send_question_to_all():
    if current_question < len(questions):
        for client_address in client_scores.keys():
            question = questions[current_question]
            server_socket.sendto(pickle.dumps(question), client_scores[client_address]['address'])
    else:
        end_game()

def receive_answers():
    global current_question
    answers_received = 0
    while answers_received < len(client_scores):
        bytes_rx, client_address = server_socket.recvfrom(1024)
        answer, client_id = pickle.loads(bytes_rx)
        correct_answer = questions[current_question]['respuesta_correcta']
        if answer == correct_answer:
            client_scores[client_address]['score'] += 1
        print(f"Respuesta recibida de {client_id}: {answer}, Puntuación actual: {client_scores[client_address]['score']}")
        answers_received += 1
    
    current_question += 1
    send_question_to_all()

def end_game():
    final_scores = "Resultados del juego: \n" + "\n".join([f"Cliente {addr}: {data['score']} puntos" for addr, data in client_scores.items()])
    for client_address in client_scores.keys():
        server_socket.sendto(pickle.dumps(final_scores), client_scores[client_address]['address'])
    print("Juego terminado.")
    server_socket.close()

# Bucle principal del servidor
while True:
    if len(client_scores) < MIN_PLAYERS:
        print("Esperando a que se conecten más jugadores...")
        data, address = server_socket.recvfrom(1024)
        if address not in client_scores:
            client_scores[address] = {'score': 0, 'address': address}
            server_socket.sendto(pickle.dumps("Conectado al servidor de juego."), address)
        if len(client_scores) == MIN_PLAYERS:
            send_question_to_all()
    else:
        receive_answers()
