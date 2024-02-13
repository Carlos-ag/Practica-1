import socket
import pickle
import sys

def send_message(client_socket, server_address, message):
    try:
        client_socket.sendto(pickle.dumps(message), server_address)
        server_response, _ = client_socket.recvfrom(4096)
        return pickle.loads(server_response)
    except Exception as e:
        print(f"Error sending message to server: {e}")
        return None

def main(server_ip, server_port, client_id):
    client_socket = socket.socket(family=socket.AF_INET, type=socket.SOCK_DGRAM)
    client_socket.settimeout(10.0)
    server_address = (server_ip, server_port)

    initial_message = {"client_id": client_id, "message": "START"}
    print("Starting game...")
    response = send_message(client_socket, server_address, initial_message)

    while True:
        if response and 'action' in response and response['action'] == 'next_question':
            response = send_message(client_socket, server_address, {"client_id": client_id, "message": "NEXT"})
            continue

        if response and 'pregunta' in response:
            print("\nNew Question:")
            print(response["pregunta"])
            for idx, option in enumerate(response["respuestas"], start=1):
                print(f"{idx}. {option}")
            user_answer = input("Your answer (number): ")
            try:
                answer_index = int(user_answer) - 1
                if answer_index < 0 or answer_index >= len(response["respuestas"]):
                    raise ValueError
                answer_message = {"client_id": client_id, "respuesta": response["respuestas"][answer_index]}
            except ValueError:
                print("Invalid answer, try again.")
                continue
            result = send_message(client_socket, server_address, answer_message)
            if result:
                print(result["message"])
            continue_game = input("Type 'EXIT' to quit or press Enter to continue: ").strip()
            if continue_game.upper() == "EXIT":
                send_message(client_socket, server_address, {"client_id": client_id, "message": "EXIT"})
                break

    client_socket.close()
    print("Game ended.")

if __name__ == "__main__":
    if len(sys.argv) != 4:
        print("Usage: python client.py <Server IP> <Server Port> <Client ID>")
    else:
        server_ip = sys.argv[1]
        server_port = int(sys.argv[2])
        client_id = sys.argv[3]
        main(server_ip, server_port, client_id)
