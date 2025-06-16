import random
import re
import google.generativeai as genai
from modules import responses, gemini

GEMINI_API_KEY = "YOUR_GEMINI_API_KEY" # Замените на ваш API ключ Gemini
genai.configure(api_key=GEMINI_API_KEY)

def stabilise_response_with_gemini(text_to_stabilize):
    """
    Sends a given text to Gemini API to get a corrected/stabilized version.
    """
    if not GEMINI_API_KEY or GEMINI_API_KEY == "YOUR_GEMINI_API_KEY":
        print("Ошибка: API ключ Gemini отсутствует. Ответ не стабилизирован.")
        return text_to_stabilize

    message_for_gemini = f"""Скорректируй, улучши и сделай более естественным мой ответ на русском языке, чтобы он звучал более дружелюбно и грамотно.
Выводи ТОЛЬКО самый верный вариант.
Также предлагай только один самый верный вариант и выводи только его без всяких "вот несколько вариантов", "блаблаблаблабла".
Вот ответ, который нужно скорректировать:
{text_to_stabilize}
"""

    try:
        model = genai.GenerativeModel('gemini-1.5-flash-latest')
        response = model.generate_content(message_for_gemini)

        if response.text:
            return response.text
        else:
            print("Предупреждение: Gemini API не вернул текст в ответе. Возможно, контент был заблокирован.")
            return text_to_stabilize

    except Exception as e:
        print(f"Ошибка при стабилизации ответа с Gemini API: {e}")
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
    global DONTUNDERSTAND
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
        return gemini.send_response_to_gemini(user_input_lower, GEMINI_API_KEY)

def messaging_with_ai():
    print("Познакомьтесь с DimonAI, который всегда рад помочь!")
    while True:
        people_word = input("Вы: ")
        initial_response = generating_response(people_word)
        stabilized_response = stabilise_response_with_gemini(initial_response)
        print("DimonAI: " + stabilized_response)

if __name__ == "__main__":
    messaging_with_ai()
