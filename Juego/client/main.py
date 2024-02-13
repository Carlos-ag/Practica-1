import socket
import struct
import threading

from cliente_tcp import init_tcp_socket, authenticate_user, close_tcp_socket
import global_variables

from pytimedinput import timedInput


def end_game(tcp_sock):
    """
    Ends the game.
    """
    close_tcp_socket(tcp_sock)
    return 0

def connect_to_udp_server(udp_ip, udp_port):
    """
    se conecta al servidor UDP
    """
    global_variables.udp_sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    global_variables.udp_sock.connect((udp_ip, udp_port))
    
    global_variables.udp_connected = True
    
    global_variables.udp_sock.sendall(global_variables.username.encode())

def handle_user_response_to_question():
    """
    maneja la respuesta del usuario a una pregunta
    """
    userText, timedOut = timedInput("Write the answer (write the full answer or the number):", global_variables.time_per_question)
    if(timedOut):
        print("\nTimed out when waiting for input.")
        global_variables.udp_sock.sendall(userText.encode())
    else:
        global_variables.udp_sock.sendall(userText.encode())
    
    print("Response sent to server.\n")
        
    
def keep_receiving_multicast_messages(sock):
    """
    mantine la recepcion de mensajes multicast
    """    
    messages_received = []
    
    while True:
        data, _ = sock.recvfrom(1024)
        if data.decode().startswith("\nScores:") or (data not in messages_received):

            messages_received.append(data)
            if (not global_variables.udp_connected) and (data.decode().startswith("UDP_SERVER:")):
                udp_ip, udp_port = data.decode().split(":")[1:]
                udp_port = int(udp_port)
                connect_to_udp_server(udp_ip, udp_port)

            elif data.decode().startswith("TIME_PER_QUESTION:"):
                global_variables.time_per_question = int(data.decode().split(":")[1])
                print(f"\nTime per question: {global_variables.time_per_question}\n")

            elif data.decode().startswith("Question"):
                print(data.decode())
                handle_user_response_to_question()
            
            elif data.decode().startswith("\nScores:"):
                
                if (not messages_received[-3].decode().startswith("\nScores:")) and (not messages_received[-2].decode().startswith("\nScores:")):
                    print(data.decode())

            
            elif data.decode().startswith("END GAME"):
                exit()
                return

                
            else:
                print(data.decode())
        

def join_multicast_group(multicast_group_ip, multicast_port):
    """
    se une a un grupo multicast para recibir mensajes
    """

    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM, socket.IPPROTO_UDP)
    sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEPORT, 1)
    # se une al grupo multicast
    sock.bind(('', multicast_port))
    group = socket.inet_aton(multicast_group_ip)
    mreq = struct.pack('4sL', group, socket.INADDR_ANY)
    sock.setsockopt(socket.IPPROTO_IP, socket.IP_ADD_MEMBERSHIP, mreq)

    
    # se inicia el hilo para recibir mensajes multicast
    print("Joined multicast group. Waiting for game data...\n")
    t = threading.Thread(target=keep_receiving_multicast_messages, args=(sock,))
    t.start()



def start_game(tcp_sock):
    """
    espera los detalles del grupo multicast del servidor y luego se une al grupo
    """
    tcp_sock.sendall("OK".encode())
    print("\nWaiting for multicast group details from server...")
    
    data = tcp_sock.recv(1024).decode()
    while data == "":
        data = tcp_sock.recv(1024).decode()
    print("Ya llego el mensaje")

    print(data)
    if data.startswith("MULTICAST_GROUP:"):
        _, multicast_group_ip, multicast_port = data.split(":")
        tcp_sock.sendall("OK".encode())
        join_multicast_group(multicast_group_ip, int(multicast_port))

    while global_variables.udp_connected == False:
        pass



def main():
    """
    punto de entrada del programa
    """
    global_variables.init()
    tcp_sock = init_tcp_socket()
    authenticated = False
    is_exitting = False
    while not authenticated and not is_exitting:
        authenticated, is_exitting = authenticate_user(tcp_sock)
        if is_exitting:
            end_game(tcp_sock)
        elif authenticated:
            start_game(tcp_sock)
            

if __name__ == "__main__":
    main()
