from authentification_functions import login_user, register_user, update_score, update_if_higher, get_ranking_scores, get_max_score, delete_user
from valid_input import enter_valid_input

def handle_authentification():
    user_logged = False
    while not user_logged:
        print("Welcome to the game")
        print("Please, log in or sign up to play")
        print("1. Log in")
        print("2. Sign up")
        print("3. Delete user")
        print("4. Exit")
        option = enter_valid_input([1, 2, 3, 4], "Choose an option: ")
        
        if option in [1, 2, 3]:
            user = input("Username: ")
            password = input("Password: ")

        if option == 1:
            
            # log in
            if login_user(user, password):
                print("Logging in...")
                print("Welcome " + user)
                print("Your current score is: " + str(get_max_score(user)))
                print("Top 5 players: ")
                print(get_ranking_scores())
                user_logged = True

        elif option == 2: # sign up
            if register_user(user, password):
                print("Signing up...") 
                print("User registered")
                user_logged = True
            else:
                print("User already exists, please log in")
        elif option == 3:

            # delete user
            if delete_user(user, password):
                print("Deleting user...")
                print("User deleted")
            else:
                print("User not found or password incorrect")    

        elif option == 4:
            print("Goodbye!")
            exit()
        else:
            print("Invalid option")
            exit()




