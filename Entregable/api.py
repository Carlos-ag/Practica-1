import random
import requests

def get_api_data():
    # 1. Realizar una llamada a la API
    url = 'https://opentdb.com/api.php?amount=5&difficulty=easy&type=multiple'

    response = requests.get(url)

    if response.status_code == 200:
        api_preguntas = response.json()
    else:
        print('Error:', response.status_code)

    return transform_data(api_preguntas)



# 2. Transformar los datos de la API en una lista de diccionarios
def transform_data(data):
    formatted_list = []
    for item in data['results']:
        all_answers = item['incorrect_answers'] + [item['correct_answer']]
        random.shuffle(all_answers)
    
        question_map = {
        "pregunta": item['question'].replace('&#039;', "'").replace('&amp;', '&'),
        "respuestas": all_answers,
        "respuesta_correcta": item['correct_answer']
    }
        formatted_list.append(question_map)
    return formatted_list
