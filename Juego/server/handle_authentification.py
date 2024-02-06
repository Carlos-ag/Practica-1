import socket 
import sys
from authentification_functions import login_user, register_user, update_score, update_if_higher, get_ranking_scores, get_max_score, delete_user
from valid_input import enter_valid_input

def handle_authentification(sock,connection):
    user_logged = False
    while not user_logged:
        connection.sendall("Welcome to the game".encode())
        connection.sendall("""Please, log in or sign up to play
        1. Log in
        2. Sign up
        3. Delete user
        4. Exit\n""".encode())

        

        option = enter_valid_input([1, 2, 3, 4],sock,connection)
        
        if option in [1, 2, 3]:
            user = connection.recv(1024) .decode()
            password = connection.recv(1024) .decode()

        if option == 1:
            
            # log in
            if login_user(user, password):
                connection.sendall("""Logging in...
                Welcome """ + user + """
                Your current score is: """ + str(get_max_score(user)) + """
                Top 5 players:
                """ + get_ranking_scores() + "\n".encode())
                user_logged = True

        elif option == 2: # sign up
            if register_user(user, password):
                connection.sendall("""Signing up...
                User registered\n""".encode())
                user_logged = True
            else:
                connection.sendall("User already exists, please log in\n".encode())
        elif option == 3:

            # delete user
            if delete_user(user, password):
                connection.sendall("User deleted\n".encode())
                user_logged = True
            else:
                connection.sendall("User does not exist\n".encode())   

        elif option == 4:
            connection.sendall("Goodbye!\n".encode())
            exit()
        
            


    connection.sendall("SUCCESFUL AUTHENTIFICATION".encode())
    return user




