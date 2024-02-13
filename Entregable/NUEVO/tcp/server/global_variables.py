def init():
    """
    Inicializa las variables globales del servidor    
    """
    global game_started
    game_started = False
    global MIN_PLAYERS
    MIN_PLAYERS = 2
    global authenticated_users
    authenticated_users = []

    global udp_sock
    udp_sock = None

    global init_time_question 
    init_time_question = 0

    global answers_received
    answers_received = 0
    
    global time_per_question
    time_per_question = 20

    

