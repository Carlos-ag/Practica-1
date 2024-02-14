import socket
import pickle
import sys

# Configuración inicial
SERVER_IP = input("Ingrese la dirección IP del servidor: ")
PORT = input("Ingrese el número de puerto del servidor: ")
try:
    PORT = int(PORT)
except ValueError:
    print("El puerto debe ser un número.")
    exit(1)

# Crear el socket UDP
client_socket = socket.socket(family=socket.AF_INET, type=socket.SOCK_DGRAM)
server_address = (SERVER_IP, PORT)

# Identificador único para este cliente
client_id = input("Ingrese su identificador de jugador (por ejemplo, Cliente1): ")

# Función para enviar respuestas al servidor
def send_answer(answer):
    message = (answer, client_id)
    client_socket.sendto(pickle.dumps(message), server_address)

# Conectarse al servidor
client_socket.sendto(pickle.dumps(f"Hola servidor, soy {client_id}"), server_address)

# Esperar confirmación de conexión
data, _ = client_socket.recvfrom(1024)
print(pickle.loads(data))

def select_valid_answer():
    selected_answer = input("Seleccione su respuesta (número): ")
    try:
        return int(selected_answer)
    except ValueError:
        print("La selección debe ser un número. Su respuesta no fue enviada.")
        return select_valid_answer()

try:
    while True:
        # Esperar pregunta del servidor
        data, _ = client_socket.recvfrom(4096)
        question = pickle.loads(data)

        if isinstance(question, str) and question.startswith("Resultados del juego"):
            print(question)
            break
        else:
            print(f"Pregunta: {question['pregunta']}")
            for idx, option in enumerate(question['respuestas'], start=1):
                print(f"{idx}. {option}")
            selected_answer = select_valid_answer()

            try:
                # Convertir la selección del usuario en la respuesta correspondiente
                answer = question['respuestas'][int(selected_answer) - 1]
                send_answer(answer)
            except (ValueError, IndexError):
                print("Selección inválida. Respuesta no enviada.")
except KeyboardInterrupt:
    print("\nJuego terminado por el usuario.")
finally:
    client_socket.close()
