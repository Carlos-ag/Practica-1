import socket 
import sys
# TODO: MIRAR SI UNCOMMENTEAR ESTO
# from ask_ip_port import ask_ip_port

def read_ip_port():
    with open("Juego/commons/ip_port.txt", "r") as file:
        ip_port = file.read().split(",")
        return (ip_port[0], int(ip_port[1]))

def init_tcp_socket():
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_address = read_ip_port()
    sock.connect(server_address)
    return sock

def close_tcp_socket(sock):
    sock.close()

def send_valid_input(sock):
    valid_answer = False
    while not valid_answer:
        user_input = input()
        sock.sendall(user_input.encode())
        data=sock.recv(1024).decode()
        if data == "OK":
            valid_answer = True
        else:
            print(data)

def handle_login_register_delete(sock):
    # Nombre de usuario
    print(sock.recv(1024).decode())
    send_valid_input(sock)

    # Contraseña
    print(sock.recv(1024).decode())
    send_valid_input(sock)


def authenticate_user(sock):
    # Mensaje de bienvenida
    print(sock.recv(1024).decode())

    # Recepción de opciones
    print(sock.recv(1024).decode())
    
    # Selección de opción
    send_valid_input(sock)

    data = sock.recv(1024).decode()
    if data in ["LOGIN", "REGISTER", "DELETE"]:
        handle_login_register_delete(sock)
    else : #EXIT
        print(data)
        sock.close()
        exit()
    
    # Mensaje de autenticación
    data = sock.recv(1024).decode()
    if data == "SUCCESSFUL AUTHENTICATION":
        return True
    else:
        return False
    






    



        
    