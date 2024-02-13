import random
import requests

def get_api_data():
    # 1. Realizar una llamada a la API
    url = 'https://opentdb.com/api.php?amount=5&difficulty=easy&type=multiple'

    response = requests.get(url)

    if response.status_code == 200:
        api_preguntas = response.json()
        return transform_data(api_preguntas)
    else:
        print('Error:', response.status_code)
        return []

    



# 2. Transformar los datos de la API en una lista de diccionarios
def transform_data(data):
    formatted_list = []
    replace_map = {
        '&#039;': "'",
        '&amp;': '&',
        '&quot;': '"',
        '&lt;': '<',
        '&gt;': '>'
    }
    for item in data['results']:
        all_answers = item['incorrect_answers'] + [item['correct_answer']]
        random.shuffle(all_answers)

        question = item['question']
        correct_answer = item['correct_answer']

        for key, value in replace_map.items():
            question = question.replace(key, value)
            correct_answer = correct_answer.replace(key, value)
            for i, answer in enumerate(all_answers):
                all_answers[i] = all_answers[i].replace(key, value)

    
        question_map = {
        "pregunta": question,
        "respuestas": all_answers,
        "respuesta_correcta": correct_answer
    }
        formatted_list.append(question_map)
    return formatted_list