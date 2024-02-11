from api import get_api_data

def init():
    global questions
    questions = get_api_data()
    global multicast_sock 
    multicast_sock = None


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
    
    # CONSTANTS
    global time_per_question
    time_per_question = 20

    global game_ended
    game_ended = False

    


