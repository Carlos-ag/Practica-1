import hashlib

USERS_FILE = "Juego/commons/users.txt"

def encode_password(password):
    """
    codifica la contraseña en sha256
    """
    return hashlib.sha256(password.encode()).hexdigest()

def login_user(user, encoded_password):
    """
    Verifica si el usuario y la contraseña son correctos
    """
    encoded_password = encode_password(encoded_password)
    with open(USERS_FILE, "r") as file:
        for line in file:
            username, password_hash, max_score = line.strip().split(",")
            if username == user and password_hash == encoded_password:
                return True
        return False

def register_user(user, password):
    """
    Registra un usuario en el archivo de usuarios
    """
    if login_user(user, password) == True:
        return False
    password = encode_password(password)
    with open(USERS_FILE, "a") as file:
        file.write(f"{user},{password},0\n")
    return True

def update_score(user, score):
    """
    Actualiza el puntaje máximo de un usuario
    """
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
    """
    Actualiza el puntaje máximo de un usuario si el puntaje actual es mayor
    """
    if get_max_score(user) < score:
        update_score(user, score)
        return True
    return False

def get_ranking_scores():
    """
    Obtiene los puntajes máximos de los usuarios y los ordena de mayor a menor
    """
    with open(USERS_FILE, "r") as file:
        lines = file.readlines()
    scores = []
    for line in lines:
        username, password_hash, max_score = line.strip().split(",")
        scores.append([username, int(max_score)])
    scores.sort(key=lambda x: x[1], reverse=True)
    return format_ranking(scores[:5])

def format_ranking(scores):
    """
    Formatea los puntajes máximos de los usuarios para mostrarlos en el ranking
    """
    return "\n".join([f"{i+1}. {user} - {score}" for i, (user, score) in enumerate(scores)])


def get_max_score(user):
    """
    Obtiene el puntaje máximo de un usuario
    """
    with open(USERS_FILE, "r") as file:
        for line in file:
            username, password_hash, max_score = line.strip().split(",")
            if username == user:
                return int(max_score)
    return 0


def delete_user(user, password):
    """
    Elimina un usuario del archivo de usuarios
    """
    password = encode_password(password)  
    found = False  
    with open(USERS_FILE, "r") as file:
        lines = file.readlines() 

    with open(USERS_FILE, "w") as file:
        for line in lines:
            username, password_hash, max_score = line.strip().split(",")
            if username == user and password_hash == password:
                found = True  
            else:
                file.write(line)  

    return found  

