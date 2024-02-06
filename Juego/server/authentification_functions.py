# library to hash the password
import hashlib

USERS_FILE = "Entregable/users.txt"

# the file is structured as:
# username, password_hash, max_score

def encode_password(password):
    return hashlib.sha256(password.encode()).hexdigest()

def login_user(user, password):
    password = encode_password(password)
    with open(USERS_FILE, "r") as file:
        print(file.readlines())
        for line in file:
            print("linea", line)
            username, password_hash, max_score = line.strip().split(",")
            if username == user and password_hash == password:
                return True
        print("he salido del for")
        return False

def register_user(user, password):
    if login_user(user, password) == True:
        return False
    password = encode_password(password)
    with open(USERS_FILE, "a") as file:
        file.write(f"{user},{password},0\n")
    return True

def update_score(user, score):
    with open(USERS_FILE, "r") as file:
        lines = file.readlines()
    with open(USERS_FILE, "w") as file:
        for line in lines:
            username, password_hash, max_score = line.strip().split(",")
            if username == user:
                file.write(f"{username},{password_hash},{max(int(max_score), score)}\n")
            else:
                file.write(line)
    return True

def update_if_higher(user, score):
    if get_max_score(user) < score:
        update_score(user, score)
        return True
    return False

def get_ranking_scores():
    # get only the top 5
    with open(USERS_FILE, "r") as file:
        lines = file.readlines()
    scores = []
    for line in lines:
        username, password_hash, max_score = line.strip().split(",")
        scores.append([username, int(max_score)])
    scores.sort(key=lambda x: x[1], reverse=True)
    return format_ranking(scores[:5])

def format_ranking(scores):
    return "\n".join([f"{i+1}. {user} - {score}" for i, (user, score) in enumerate(scores)])


def get_max_score(user):
    with open(USERS_FILE, "r") as file:
        for line in file:
            username, password_hash, max_score = line.strip().split(",")
            if username == user:
                return int(max_score)
    return 0


def delete_user(user, password):
    password = encode_password(password)  # Encode the provided password
    found = False  # Flag to check if the user was found and deleted
    with open(USERS_FILE, "r") as file:
        lines = file.readlines()  # Read all lines from the file

    with open(USERS_FILE, "w") as file:
        for line in lines:
            username, password_hash, max_score = line.strip().split(",")
            if username == user and password_hash == password:
                found = True  # User found and will be deleted (by not writing this line back)
            else:
                file.write(line)  # Write back all lines except the one to be deleted

    return found  # Return True if user was found and deleted, else False

