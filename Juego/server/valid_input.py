def enter_valid_input(list,sock,connection):
    
    number = connection.recv(1024).decode()

    while not number.isdigit() or int(number) not in list:
        connection.sendall("Ingrese un número válido".encode())
        number = connection.recv(1024).decode()
    
    return int(number)