def init():
    global username
    username = ""
    global time_per_question
    time_per_question = 20

    global udp_connected
    udp_connected = False

    global udp_sock
    udp_sock = None