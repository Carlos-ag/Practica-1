import socket 
import sys
from handle_authentification import handle_authentification  
import os

def read_ip_port():
    with open("Juego/commons/ip_port.txt", "r") as file:
        ip_port = file.read().split(",")
        return (ip_port[0], int(ip_port[1]))

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
