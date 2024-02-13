import socket 
import sys
from authentification_functions import login_user, register_user, update_score, update_if_higher, get_ranking_scores, get_max_score, delete_user
import global_variables
import threading

def enter_valid_input(list,connection):
    """
    esta función recibe una seleccion de una conexión, y se encarga de comprobar si el número ingresado es válido para el menú de opciones
    
    """
    user_state = ["LOGIN", "REGISTER", "DELETE", "EXIT"]
    number = connection.recv(1024).decode()

    while not number.isdigit() or int(number) not in list:
        connection.sendall("Ingrese un número válido".encode())
        number = connection.recv(1024).decode()
    
    connection.sendall(user_state[int(number)-1].encode())

    return int(number)


def send_data(data, connection):
    """
    esta función recibe un mensaje y una conexión, y se encarga de enviar el mensaje a la conexión
    """
    connection.sendall(data.encode())



def handle_client_connection(client_socket):
    """
    esta función recibe un socket de un cliente, y se encarga de manejar la autenticación del usuario, además de manejar el inicio del juego
    """
    try:
        username, connection_user = handle_authentification(client_socket)
        user = {
            "username": username,
            "connection_tcp": connection_user,
            "score": 0,
        }
        if user:  
            with threading.Lock():  
                try: 
                    global_variables.authenticated_users.append(user)
                    

                    print(client_socket.recv(1024).decode() + " from " + username)

                    if (len(global_variables.authenticated_users) >= global_variables.MIN_PLAYERS) and not global_variables.game_started:

                        global_variables.game_started = True
                        for user in global_variables.authenticated_users:
                            try:
                                user['connection_tcp'].sendall("GAME STARTS".encode())
                            except:
                                print(user)
                                continue         
                except Exception as e:
                    print("Error during client handling: ", e)

    except Exception as e:
        print("Error during client handling: ", e)
    

user_state = ["LOGIN", "REGISTER", "DELETE", "EXIT"]

def handle_authentification(connection):
    """
    esta función recibe una conexión, y se encarga de manejar la autenticación del usuario, además de manejar el inicio del juego
    """
    user_logged = False
    send_data("Welcome to the game" + "\n\n", connection)
    error = False
    while not user_logged and not error:
        send_data(
        """Please, log in or sign up to play
        1. Log in
        2. Sign up
        3. Delete user
        4. Exit\n\n""", connection)

        print("Waiting for user input...")
        option = enter_valid_input([1, 2, 3, 4],connection)
        data = connection.recv(1024).decode()
        if data != "OK":
            print("ERROR")
            error = True

        
        if option == 4:
            connection.sendall("EXIT".encode())
            connection.close()

            
        

        if option in [1, 2, 3]:
            connection.sendall("Enter your username: ".encode())
            user = connection.recv(1024).decode()
            connection.sendall("Enter your password: ".encode())
            password = connection.recv(1024) .decode()
        
    


        if option == 1:

            # log in
            if login_user(user, password):
                connection.sendall("SUCCESSFUL AUTHENTICATION".encode())
                user_logged = True
                return user, connection
            else:
                connection.sendall("User does not exist or password is incorrect\n".encode())

        elif option == 2: # sign up
            if register_user(user, password):
                connection.sendall("SUCCESSFUL AUTHENTICATION".encode())
                user_logged = True
                return user, connection
            else:
                connection.sendall("User already exists, please log in\n".encode())
        elif option == 3:
            # delete user
            if delete_user(user, password):
                connection.sendall("USER DELETED".encode())
            else:
                connection.sendall("User does not exist\n".encode())   





