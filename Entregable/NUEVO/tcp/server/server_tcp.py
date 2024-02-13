import socket 
import sys
from handle_authentification import handle_authentification  
import os

def read_ip_port():
    """
    Lee el archivo ip_port.txt y retorna la IP y el puerto del servidor
    """
    print(os.getcwd())

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
    Inicializa el socket del servidor
    """
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_address = read_ip_port()
    sock.bind(server_address)
    sock.listen(5)  
    return sock
