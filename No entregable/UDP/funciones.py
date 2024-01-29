def ask_IP_address():
    valid_IP = False
    while not valid_IP:
        IP_address = input("Enter the IP address: ")
        try:
            socket.inet_aton(IP_address)
            valid_IP = True
        except:
            print("Invalid IP address")
    return IP_address

def ask_port_number():
    valid_port = False
    while not valid_port:
        port_number = input("Enter the port number: ")
        try:
            port_number = int(port_number)
            if port_number > 0 and port_number < 65535:
                valid_port = True
            else:
                print("Invalid port number")
        except:
            print("Invalid port number")
    return port_number

def ask_message():
    msg = input("Enter a message: ")
    return msg

def ask_number_client():
    number_client = random.randint(1, 1000)
    return number_client
