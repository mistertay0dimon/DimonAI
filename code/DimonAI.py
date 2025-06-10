import random
import re
import requests
import json
from modules import responses

GEMINI_API_KEY = "YOUR_GEMINI_API_KEY" # Замените на ваш API ключ Gemini
GEMINI_API_ENDPOINT = "https://generativelanguage.googleapis.com/v1beta/models/gemini-2.5-flash-preview-05-20:generateContent"

def stabilise_response_with_gemini(text_to_stabilize):
    """
    Sends a given text to Gemini API to get a corrected/stabilized version.
    """
    if not GEMINI_API_KEY or GEMINI_API_KEY == "YOUR_GEMINI_API_KEY":
        print("Error: Gemini API key is missing. Then, response not stabilised.")
        return text_to_stabilize

    message_for_gemini = f"""Скорректируй, улучши и сделай более естественным мой ответ на русском языке, чтобы он звучал более дружелюбно и грамотно
Выводи ТОЛЬКО самый верный вариант.
Также предлагай только один самый веееееееееееееееееерный вариант и выводи только его без всяких вот несколько вариантов блаблаблаблабла
Вот ответ который нужно скорректировать:
{text_to_stabilize}
"""

    payload = {
        "contents": [
            {
                "parts": [
                    {"text": message_for_gemini}
                ]
            }
        ]
    }
    headers = {
        "Content-Type": "application/json"
    }

    try:
        response = requests.post(
            f"{GEMINI_API_ENDPOINT}?key={GEMINI_API_KEY}",
            headers=headers,
            data=json.dumps(payload)
        )
        response.raise_for_status()

        response_data = response.json()

        if "candidates" in response_data and len(response_data["candidates"]) > 0:
            for candidate in response_data["candidates"]:
                if "content" in candidate and "parts" in candidate["content"]:
                    for part in candidate["content"]["parts"]:
                        if "text" in part:
                            return part["text"]
        else:
            print("Error stabilise response")
            return text_to_stabilize

    except requests.exceptions.RequestException as e:
        print(f"Error: {e}")
        return text_to_stabilize
    except json.decoder.JSONDecodeError as e:
        print(f"Error decoing JSON response with stabilised response: {e}")
        return text_to_stabilize
    except Exception as e:
        print(f"Unkown error excepted with stabilise response: {e}")
        return text_to_stabilize

IS_GREETED = "no"
HOWAREUSER_PARTS = [
    "хорошо",
    "нормально",
    "отлично",
    "просто супер",
    "супер",
    "офигенно"
]

def generating_response(user_input):
    global IS_GREETED

    user_input_lower = user_input.lower()

    if "сложи" in user_input_lower or "+" in user_input_lower:
        try:
            numbers = re.findall(r'\d+', user_input)
            if len(numbers) >= 2:
                num1 = float(numbers[0])
                num2 = float(numbers[1])
                result = num1 + num2
                return f"Ответ: {result}"
            else:
                return "Не могу понять числа для сложения. Пожалуйста, введите два числа."
        except ValueError:
            return "Ошибка при обработке чисел. Убедитесь, что вы вводите корректные числа."

    if user_input_lower == "привет":
        if IS_GREETED == "yes":
            beta_response = random.choice(responses.YOUHELLOLED_MASSIVE)
            final_response = "Я вижу, что ты опять со мной здороваешься. " + beta_response
            return final_response
        else:
            IS_GREETED = "yes"
            beta_response = random.choice(responses.HELLO_MASSIVE)
            GenerateTwoMassive_Format1 = random.choice(HOWAREUSER_PARTS)
            if beta_response == "ики!":
                final_response = "Привет" + beta_response
                return final_response
            elif beta_response == "как дела? Лично у меня все ":
                final_response = "Привет, " + beta_response + GenerateTwoMassive_Format1
                return final_response
            else:
                final_response = "Привет, " + beta_response
                return final_response

    elif user_input_lower == "пока":
        beta_response = random.choice(responses.BYE_MASSIVE)
        final_response = "До встречи" + beta_response
        return final_response
    elif user_input_lower == "нормально":
        beta_response = random.choice(responses.NORMALDELA_MASSIVE)
        final_response = "Нормально" + beta_response
        return final_response
    elif user_input_lower == "как дела":
        beta_response = random.choice(responses.HOWAREYOU_MASSIVE)
        final_response = "Нормально" + beta_response
        return final_response
    elif any(phrase in user_input_lower for phrase in ["ты талантливый", "ты молодец", "отличная идея", "впечатляет"]):
        beta_response = random.choice(responses.COMPLIMENTS_MASSIVE)
        final_response = beta_response
        return final_response
    elif any(phrase in user_input_lower for phrase in ["кто ты", "что ты", "ты кто", "что ты такое"]):
        beta_response = random.choice(responses.QUESTION_ABOUT_BOT_MASSIVE)
        final_response = beta_response
        return final_response
    elif any(phrase in user_input_lower for phrase in ["согласен", "именно так", "так и есть"]):
        beta_response = random.choice(responses.AGREEMENT_MASSIVE)
        final_response = beta_response
        return final_response
    else:
        return "Эх, жаль, я не понимаю это. Мой создатель Димон обязательно научит меня и добавит список слов для этого слова!"


def messaging_with_ai():
    print("Познакомьтесь с DimonAI, который всегда рад помочь!")
    while True:
        people_word = input("Вы: ")
        if people_word.lower() in ["выход", "exit", "quit"]:
            print("DimonAI: Пока-пока! Буду ждать тебя снова.")
            break
        initial_response = generating_response(people_word)
        stabilized_response = stabilise_response_with_gemini(initial_response)
        print("DimonAI: " + stabilized_response)

if __name__ == "__main__":
    messaging_with_ai()
