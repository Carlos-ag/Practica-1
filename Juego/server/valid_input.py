def enter_valid_input(list,sock,connection):
    user_state = ["LOGIN", "REGISTER", "DELETE", "EXIT"]
    number = connection.recv(1024).decode()

    while not number.isdigit() or int(number) not in list:
        connection.sendall("Ingrese un número válido".encode())
        number = connection.recv(1024).decode()
    
    connection.sendall(user_state[int(number)-1].encode())

    return int(number)