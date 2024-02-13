import socket
import threading
from server_tcp import read_ip_port, init_tcp_socket
import struct
from handle_authentification import handle_authentification
import time
from api import get_api_data
import global_variables
from copy import deepcopy

authenticated_users = []
users_lock = threading.Lock()
global MIN_PLAYERS
MIN_PLAYERS = 2
multicast_group_ip = '224.1.1.1'
multicast_port = 5001

is_last_question = False

udp_ip = "127.0.0.1"
udp_port = 5005

global game_started
game_started = False




def handle_client_connection(client_socket):
    """
    maneja la conexión con el cliente y lo autentifica
    """
    global min_players
    global game_started
    try:
        if len(authenticated_users) >= MIN_PLAYERS:
            client_socket.sendall("GAME ALREADY STARTED TRY AGAIN LATER".encode())
            print("Game already started for user {}".format(client_socket.getpeername()))
            client_socket.close()
            while True:
                pass

        else:   
            username, connection_user = handle_authentification(client_socket)
            if username != None:
                user = {
                    "username": username,
                    "connection_tcp": connection_user,
                    "score": 0,
                }
                if user:  
                    with users_lock:  
                        authenticated_users.append(user)
                        print(client_socket.recv(1024).decode())
                        if (len(authenticated_users) >= MIN_PLAYERS) and (not game_started):
                            game_started = True
                            start_multicast()

                   
                    
    except Exception as e:
        print("Error during client handling: ", e)
    finally:
        if global_variables.game_ended:
            client_socket.close()
            global_variables.game_started = False
            return 

def send_multicast_message(multicast_sock, message):
    """
    mandar un mensaje a todos los usuarios conectados
    """
    multicast_sock.sendto(message.encode(), (multicast_group_ip, multicast_port)) 



def compute_score(time_to_answer):
    """
    calcula el puntaje de un usuario en base al tiempo que le tomo responder
    """
    return round(10 * (1 - time_to_answer / 20), 2)



def receive_answers_from_users(user_index, correct_answer, correct_answer_index):
    """
    recibe las respuestas de los usuarios y calcula el puntaje
    """
    while True:
        data, addr = global_variables.udp_sock.recvfrom(1024)
        if data.decode() == "STOP" and addr == (udp_ip, udp_port):
            if is_last_question:
                end_game()
                print("he ejecutado end_game")
            break

        
        print(f"Received UDP message from {addr}: {data.decode()}")
        global_variables.answers_received+=1

        # se busca el usuario que envio la respuesta y se le asigna el puntaje correspondiente
        for user in authenticated_users:
            if user['udp_address'] == addr:
                user_answer = data.decode()
                if user_answer != "":
                    if (user_answer == correct_answer) or ((int(user_answer)-1) == correct_answer_index):
                        user['score'] += compute_score(time.time() - global_variables.init_time_question)
                        print(f"User {user['username']} answered correctly")
                    else:
                        print(f"User {user['username']} answered incorrectly")
                else:
                    print(f"User {user['username']} did not answer")
                break



    

def start_questions_game(authenticated_users):
    """
    inicia el juego y envia las preguntas a los usuarios
    """

    threads_list = []

    for i in range(len(global_variables.questions)):
        question = global_variables.questions[i]
        message = f"Question {i + 1}: {question['pregunta']}\n"
        for k, respuesta in enumerate(question["respuestas"], 1):
            message += f"{k}. {respuesta}\n"
        
        print("\n")
        if i == (len(global_variables.questions) - 1):
            send_multicast_message(global_variables.multicast_sock, "Last question!")

        send_multicast_message(global_variables.multicast_sock, message)

        respuesta_correcta = question["respuesta_correcta"]
        index = question["respuestas"].index(respuesta_correcta)

        global_variables.init_time_question = time.time()
        global_variables.answers_received = 0
        t = threading.Thread(target=receive_answers_from_users, args=(index, respuesta_correcta, index))
        t.start()
        
        
        while (time.time() - global_variables.init_time_question < global_variables.time_per_question) and (global_variables.answers_received < len(authenticated_users)):
            pass
        # se detiene el hilo que recibe las respuestas
        global_variables.udp_sock.sendto("STOP".encode(), (udp_ip, udp_port))
        send_multicast_message(global_variables.multicast_sock, "TIME OVER FOR QUESTION {}\n".format(i + 1))
        send_multicast_message(global_variables.multicast_sock, f"The correct answer is answer {index + 1}: {respuesta_correcta}")

        scores = "\nScores:\n"
        for user in authenticated_users:
            scores += f"{user['username']}: {user['score']}\n"
        send_multicast_message(global_variables.multicast_sock, scores)

        # se espera 5 segundos para la siguiente pregunta
        if i < len(global_variables.questions) - 1:
            send_multicast_message(global_variables.multicast_sock, f"Get ready for question {i + 2} in 5 seconds...\n")
            time.sleep(5)
        else: 
            end_game()
        


    

def stablish_udp_connection():
    """
    establece la conexión UDP con los usuarios
    """

    multicast_sock = global_variables.multicast_sock
    global_variables.udp_sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    global_variables.udp_sock.bind((udp_ip, udp_port))
    print("UDP socket is listening on {}:{}".format(udp_ip, udp_port))

    send_multicast_message(multicast_sock, f"UDP_SERVER:{udp_ip}:{udp_port}")

    # se espera a que todos los usuarios se conecten
    connected_users = 0
    while connected_users < len(authenticated_users):
        data, addr = global_variables.udp_sock.recvfrom(1024)
        print(f"Received UDP connection from {addr}")
        for user in authenticated_users:
            if user['username'] == data.decode():
                user['udp_address'] = addr
                connected_users += 1
                break

    
    time_to_answer = global_variables.time_per_question
    
    send_multicast_message(multicast_sock, f"TIME_PER_QUESTION:{time_to_answer}")
    




def end_game():
    """
    finaliza el juego y muestra el podio
    """
    global_variables.game_ended = True
    send_multicast_message(global_variables.multicast_sock, "\n\nGame over!")
    send_multicast_message(global_variables.multicast_sock, "\nThanks for playing!")
    send_multicast_message(global_variables.multicast_sock, "\n\nPodium:\n")
    authenticated_users.sort(key=lambda x: x['score'], reverse=True)
    for user in authenticated_users:
        send_multicast_message(global_variables.multicast_sock, f"{user['username']}: {user['score']}")

    send_multicast_message(global_variables.multicast_sock, "\nBye!")
    send_multicast_message(global_variables.multicast_sock, "END GAME")

    try:
        global game_started
        game_started = False
        global_variables.multicast_sock.close()
        global_variables.udp_sock.close()
        global_variables.init()
        print("Game finished")
        print("Server is shutting down.")
        for user in authenticated_users:
            user['connection_tcp'].close()
        return 0
    except:
        exit()



def start_game():
    """
    inicia el juego
    """

    stablish_udp_connection()
    start_questions_game(authenticated_users)
    

def intro_messages_game_multicast():
    """
    envia mensajes de introducción al juego a los usuarios conectados
    """
    multicast_sock = global_variables.multicast_sock
    print("entering start_game_multicast")
    send_multicast_message(multicast_sock, "Let's starts the game!")
 
    for i in range(5):
        message = f"GAME STARTS IN {5 - i} SECONDS..."
        time.sleep(1)
        send_multicast_message(multicast_sock, message)
    
    time.sleep(1)
    send_multicast_message(multicast_sock, "GAME STARTS")

    

def start_multicast():
    """
    inicia el multicast
    """
    sock = start_multicast_group()
    global_variables.multicast_sock = sock
    send_multicast_information_to_users()
    intro_messages_game_multicast()
    start_game()




def start_multicast_group():
    """
    empieza el grupo multicast para enviar mensajes a todos los usuarios conectados
    """
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    ttl = struct.pack('b', 1)
    sock.setsockopt(socket.IPPROTO_IP, socket.IP_MULTICAST_TTL, ttl)

    return sock

    

 
    


def send_multicast_information_to_users():
    """
    envia la información del grupo multicast a los usuarios conectados
    """
   
    info_message = f"MULTICAST_GROUP:{multicast_group_ip}:{multicast_port}"
    print(f"Sending multicast info to {len(authenticated_users)} users...")

    for user in authenticated_users:
        print(user)
        try:
            user_socket = user['connection_tcp']
            user_socket.sendall(info_message.encode())
            print(user_socket.recv(1024).decode())
            
        except Exception as e:
            print(f"Failed to send multicast info to {user['username']}: {e}")
        
    
def main():
    """
    función principal del servidor
    """
    global game_started
    global_variables.init()


    server_socket = init_tcp_socket()
    print("Server is listening on {}".format(server_socket.getsockname()))

    # se espera a que se conecten los usuarios mientras el juego no haya empezado
    try:
        while not game_started:
            connection, client_address = server_socket.accept()
        
            connection.settimeout(None)
            print(f"Connection from {client_address} has been established.")
            client_tcp_thread = threading.Thread(target=handle_client_connection, args=(connection,))
            client_tcp_thread.start() 
        
     
    except KeyboardInterrupt:
        print("Server is shutting down.")
    finally:
        server_socket.close()
        return

if __name__ == "__main__":
    main()
