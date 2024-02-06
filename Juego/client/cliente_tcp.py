import socket 
import sys
# TODO: MIRAR SI UNCOMMENTEAR ESTO
# from ask_ip_port import ask_ip_port

def read_delimiter():
    nombre_archivo = "Juego/commons/delimiter.txt"
    # Variables para almacenar el delimitador
    

    # Abrir el archivo para leer
    with open(nombre_archivo, 'r') as archivo:
        # the file contains only one line, that is the delimiter
        return archivo.readline().strip()

global delimiter
delimiter = read_delimiter()

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
    # Nombre de usuario
    print(sock.recv(1024).decode())
    send_valid_input(sock)

    # Contraseña
    print(sock.recv(1024).decode())
    send_valid_input(sock)

def receive_messages(sock):
    global delimiter
    data = ""
    messages = []
    print("voy a recibir")
    while True:
        chunk = sock.recv(4096).decode('utf-8')  # Receive data from the socket
        print("datos recibidos")
        print(chunk)

        if not chunk:
            break  # If no data is received, exit the loop
        data += chunk
        while delimiter in data:  # Check for the delimiter in the accumulated data
            msg, delimiter, data = data.partition(delimiter)  # Split at the first occurrence of the delimiter
            messages.append(msg)  # Add the extracted message to the list
        return messages


def send_valid_input(sock):
    valid_answer = False
    while not valid_answer:
        user_input = input()
        sock.sendall(user_input.encode())
        data = receive_messages(sock)

        if data[0] == "OK":
            valid_answer = True
            return data[1]
        else:
            print(data)

def authenticate_user(sock):
    # Mensaje de bienvenida y opciones
    print("principio")
    data = receive_messages(sock)
    print("datos recibidos")
    for message in data:
        print(message)

    
    # Selección de opción
    option_selected = send_valid_input(sock)

    if option_selected in ["LOGIN", "REGISTER", "DELETE"]:
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
    






    



        
    