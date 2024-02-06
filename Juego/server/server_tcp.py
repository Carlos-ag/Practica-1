import socket 
import sys
from handle_authentification import handle_authentification  
import os

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

def close_connection(sock,connection):
    connection.close()
    sock.close()
    exit()

def main():
    # Create a TCP/IP socket
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_address = read_ip_port()
    sock.bind(server_address)
    sock.listen(1)
    connection, client_address = sock.accept()
    data = ""
    while True:
        
        user = handle_authentification(sock,connection)

    close_connection(sock,connection)
    

if __name__ == "__main__":
    main()
