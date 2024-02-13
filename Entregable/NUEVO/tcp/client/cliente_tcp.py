import socket 
import sys

global user_state
user_state = ["LOGIN", "REGISTER", "DELETE", "EXIT"]

def read_ip_port():
    """
    Lee el archivo de configuración y retorna la IP y el puerto del servidor.
    """
    nombre_archivo = "Entregable/NUEVO/tcp/commons/ip_port.txt"

    ip_servidor = ""
    puerto_servidor = ""

    with open(nombre_archivo, 'r') as archivo:
        for linea in archivo:
            if 'SERVER' in linea:
                partes = linea.split(',')
                ip_servidor = partes[1].strip()
                puerto_servidor = partes[2].strip()
                break  
    return (ip_servidor, int(puerto_servidor))


def init_tcp_socket():
    """
    Inicializa un socket TCP y se conecta al servidor.
    """
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_address = read_ip_port()
    sock.connect(server_address)
    return sock

def close_tcp_socket(sock):
    """
    Cierra el socket TCP.
    """
    sock.close()


def handle_login_register_delete(sock):
    """
    Función que maneja el login, registro y eliminación de usuarios.
    """
    # username
    print(sock.recv(1024).decode())
    user_name = input()
    sock.sendall(user_name.encode())

    # password
    print(sock.recv(1024).decode())
    password = input()
    sock.sendall(password.encode())
    

def send_valid_input(sock):
    """
    Función que envía una opción válida al servidor.
    """
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

def end_game(tcp_sock):
    """
    Función que maneja el fin del juego.
    """
    close_tcp_socket(tcp_sock)
    return 0

def authenticate_user(sock):
    """
    Función que maneja la autenticación del usuario.
    """


    # Mensaje de bienvenida y opciones
    data = sock.recv(1024).decode()
    print(data)

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
    print(data)
    if data == "SUCCESSFUL AUTHENTICATION":
        return True, False
    elif data == "USER DELETED":
        print("\nUser deleted\n\n")
        return False, False
    else:
        print(data)
        return False, False
    






    



        
    