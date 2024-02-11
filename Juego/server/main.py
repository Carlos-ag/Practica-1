import socket
import threading
from server_tcp import read_ip_port, init_tcp_socket
import struct
from handle_authentification import handle_authentification
import time
from api import get_api_data
import global_variables

# Shared structure for authenticated users with a threading lock for thread-safe access
authenticated_users = []
users_lock = threading.Lock()
global MIN_PLAYERS
MIN_PLAYERS = 2
multicast_group_ip = '224.1.1.1'
multicast_port = 5008

is_last_question = False

udp_ip = "127.0.0.1"
udp_port = 5005

global game_started
game_started = False


def handle_client_connection(client_socket):
    global min_players
    global game_started
    try:
        if len(authenticated_users) >= MIN_PLAYERS:
            # send "GAME ALREADY STARTED TRY AGAIN LATER"
            client_socket.sendall("GAME ALREADY STARTED TRY AGAIN LATER".encode())
            print("Game already started for user {}".format(client_socket.getpeername()))
            # close connection
            client_socket.close()
            while True:
                pass

        else:   
            username, connection_user = handle_authentification(client_socket)
            user = {
                "username": username,
                "connection_tcp": connection_user,
                "score": 0,
            }
            if user:  # Assuming handle_authentification returns a user object on success
                with users_lock:  # Ensure thread-safe modification of the authenticated_users list
                    authenticated_users.append(user)
                    # recv OK from client
                    print(client_socket.recv(1024).decode())
                    if (len(authenticated_users) >= MIN_PLAYERS) and (not game_started):
                        game_started = True
                        start_multicast()

                   
                    
    except Exception as e:
        print("Error during client handling: ", e)
    finally:
        client_socket.close()
        return 

def send_multicast_message(multicast_sock, message):
    multicast_sock.sendto(message.encode(), (multicast_group_ip, multicast_port)) 



def compute_score(time_to_answer):
    # round to 2 decimal places
    # return 10 * (1 - time_to_answer / 20)
    return round(10 * (1 - time_to_answer / 20), 2)



def receive_answers_from_users(user_index, correct_answer, correct_answer_index):
    # in this function you will have to receive the answers from the users
    # and then you will have to compute the score of each user
    # when the time is over you will receive a UDP message from the server to stop the thread
    # HHHADFKLHALSKDJLÑAKSJDÑLKJASFÑLKJFÑLKJ
    # while answers_received < len(authenticated_users):
    while True:
        data, addr = global_variables.udp_sock.recvfrom(1024)
        
        # if data.decode() == "STOP" and addr is the server address
        # stop the thread
        if data.decode() == "STOP" and addr == (udp_ip, udp_port):
            if is_last_question:
                end_game()
                print("he ejecutado end_game")
            break

        
        print(f"Received UDP message from {addr}: {data.decode()}")
        global_variables.answers_received+=1

        # check if the address is in the authenticated_users list
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

    threads_list = []

    for i in range(len(global_variables.questions)):
        question = global_variables.questions[i]
        message = f"Question {i + 1}: {question['pregunta']}\n"
        for k, respuesta in enumerate(question["respuestas"], 1):
            message += f"{k}. {respuesta}\n"
        
        print("\n")

        # if last question, send a multicast message saying last question!
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

        global_variables.udp_sock.sendto("STOP".encode(), (udp_ip, udp_port))

        # send in multicast the correct answer
        send_multicast_message(global_variables.multicast_sock, "TIME OVER FOR QUESTION {}\n".format(i + 1))
        send_multicast_message(global_variables.multicast_sock, f"The correct answer is answer {index + 1}: {respuesta_correcta}")

        # now send the scores of the users
        scores = "\nScores:\n"
        for user in authenticated_users:
            scores += f"{user['username']}: {user['score']}\n"
        send_multicast_message(global_variables.multicast_sock, scores)

        # wait for 5 seconds
        if i < len(global_variables.questions) - 1:
            send_multicast_message(global_variables.multicast_sock, f"Get ready for question {i + 2} in 5 seconds...\n")
            time.sleep(5)
        else: 
            end_game()
        


    

def stablish_udp_connection():
    # you will have to stablish a connection with all the authenticated_users
    # for that you will have to create a new UDP socket and then create a new thread to handle the connection for each user
    # you will send the udp address with multicast to the users

    multicast_sock = global_variables.multicast_sock

    global_variables.udp_sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    global_variables.udp_sock.bind((udp_ip, udp_port))
    print("UDP socket is listening on {}:{}".format(udp_ip, udp_port))

    send_multicast_message(multicast_sock, f"UDP_SERVER:{udp_ip}:{udp_port}")

    # listen for the users and stablish the connection
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
    stablish_udp_connection()
    start_questions_game(authenticated_users)
    

def intro_messages_game_multicast():
    multicast_sock = global_variables.multicast_sock
    print("entering start_game_multicast")
    # Send data to the multicast group
    send_multicast_message(multicast_sock, "Let's starts the game!")
 
    for i in range(5):
        message = f"GAME STARTS IN {5 - i} SECONDS..."
        time.sleep(1)
        send_multicast_message(multicast_sock, message)
    
    time.sleep(1)
    send_multicast_message(multicast_sock, "GAME STARTS")

    

def start_multicast():
    sock = start_multicast_group()
    global_variables.multicast_sock = sock
    send_multicast_information_to_users()
    intro_messages_game_multicast()
    start_game()




def start_multicast_group():
    """
    Starts a multicast group to send messages to all connected clients.
    """

    # Create the socket
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

    # Set the time-to-live for messages to 1 so they don't go past the local network segment
    ttl = struct.pack('b', 1)
    sock.setsockopt(socket.IPPROTO_IP, socket.IP_MULTICAST_TTL, ttl)

    return sock

    

 
    


def send_multicast_information_to_users():
   
    # Inform all authenticated users about the multicast group
    info_message = f"MULTICAST_GROUP:{multicast_group_ip}:{multicast_port}"
    print(f"Sending multicast info to {len(authenticated_users)} users...")

    for user in authenticated_users:
        print(user)
        try:
            # Assuming each 'user' object has a reference to its TCP socket
            user_socket = user['connection_tcp']
            user_socket.sendall(info_message.encode())
            # recv OK from client
            print(user_socket.recv(1024).decode())
            
        except Exception as e:
            print(f"Failed to send multicast info to {user['username']}: {e}")
        
    








def main():
    global game_started
    global_variables.init()


    server_socket = init_tcp_socket()
    print("Server is listening on {}".format(server_socket.getsockname()))

    try:
        while not game_started:
            connection, client_address = server_socket.accept()
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
