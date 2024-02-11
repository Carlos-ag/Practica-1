import socket 
import sys
import global_variables
# TODO: MIRAR SI UNCOMMENTEAR ESTO
# from ask_ip_port import ask_ip_port
global user_state
user_state = ["LOGIN", "REGISTER", "DELETE", "EXIT"]

def read_ip_port():
    nombre_archivo = "Juego/commons/ip_port.txt"

    # Variables para almacenar la IP y el puerto del servidor
    ip_servidor = ""
    puerto_servidor = ""

    # Abrir el archivo para leer
    with open(nombre_archivo, 'r') as archivo:
        for linea in archivo:
            # Verificar si la línea contiene la palabra 'SERVER'
            if 'SERVER' in linea:
                # Partir la línea por las comas y quitar espacios en blanco
                partes = linea.split(',')
                ip_servidor = partes[1].strip()
                puerto_servidor = partes[2].strip()
                break  # No es necesario continuar si ya encontramos el servidor

    return (ip_servidor, int(puerto_servidor))


def init_tcp_socket():
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_address = read_ip_port()
    sock.connect(server_address)
    return sock

def close_tcp_socket(sock):
    sock.close()


def handle_login_register_delete(sock):
    # username
    print(sock.recv(1024).decode())
    user_name = input()
    sock.sendall(user_name.encode())
    global_variables.username = user_name

    # password
    print(sock.recv(1024).decode())
    password = input()
    sock.sendall(password.encode())
    

def send_valid_input(sock):
    global user_state
    valid_answer = False
    while not valid_answer:
        user_input = input()
        sock.sendall(user_input.encode())
        data = sock.recv(1024).decode()

        if data in user_state:
            valid_answer = True
            return data
        else:
            print(data)

def authenticate_user(sock):
    # Mensaje de bienvenida y opciones
    data = sock.recv(1024).decode()
    print(data)

    if data == "GAME ALREADY STARTED TRY AGAIN LATER":
        return False, True

    # Selección de opción

    option_selected = send_valid_input(sock)


    if option_selected in user_state:
        sock.sendall("OK".encode())
    else:
        print("ERROR")
        return False, True

    if option_selected in ["LOGIN", "REGISTER", "DELETE"]:
        handle_login_register_delete(sock)
    else : #EXIT
        return False, True
        
        
    
    # Mensaje de autenticación
    data = sock.recv(1024).decode()
    print("\n"+data)
    if data == "SUCCESSFUL AUTHENTICATION":
        return True, False
    elif data == "USER DELETED":
        print("\nUser deleted\n\n")
        return False, False
    else:
        print(data)
        return False, False
    
