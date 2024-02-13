import socket 
import sys
from authentification_functions import login_user, register_user, update_score, update_if_higher, get_ranking_scores, get_max_score, delete_user
from valid_input import enter_valid_input

def read_delimiter():
    """
    Lee el delimitador de un archivo de texto
    """
    nombre_archivo = "Juego/commons/delimiter.txt"
    with open(nombre_archivo, 'r') as archivo:
        return archivo.readline().strip()

delimiter = read_delimiter()

def send_data(data, connection):
    """
    Envia un mensaje al cliente
    """
    connection.sendall(data.encode())


user_state = ["LOGIN", "REGISTER", "DELETE", "EXIT"]

def handle_authentification(connection):
    """
    Maneja la autenticacion, registro y eliminacion de usuarios
    """
    user_logged = False
    send_data("Welcome to the game" + "\n\n", connection)
    error = False
    try:
        while not user_logged and not error:
            send_data(
            """Please, log in or sign up to play
            1. Log in
            2. Sign up
            3. Delete user
            4. Exit\n\n""", connection)

            print("Le pido al cliente que ingrese un numero")
            option = enter_valid_input([1, 2, 3, 4],connection)

            data = connection.recv(1024).decode()
            if data != "OK":
                print("ERROR")
                error = True

            
            if option == 4:
                connection.sendall("EXIT".encode())
                
            

            if option in [1, 2, 3]:
                connection.sendall("Enter your username: ".encode())
                user = connection.recv(1024).decode()
                connection.sendall("Enter your password: ".encode())
                password = connection.recv(1024) .decode()
            
        


            if option == 1:# log in
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
            elif option == 3:# delete user
                if delete_user(user, password):
                    connection.sendall("USER DELETED".encode())
                else:
                    connection.sendall("User does not exist\n".encode())   

    except Exception as e:
        print(e)
        return None, None





