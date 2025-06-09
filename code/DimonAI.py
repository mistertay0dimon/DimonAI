import random
import re
from modules import responses

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
    if "сложи" in user_input.lower() or "+" in user_input:
        try:
            numbers = re.findall(r'\d+', user_input)
            if len(numbers) >= 2:
                num1 = float(numbers[0])
                num2 = float(numbers[1])
                result = num1 + num2
                return f"Ответ: {result}"
            else:
                return "Не могу понять числа"
        except ValueError:
            return "Ошибка при обработке чисел"

    if user_input.lower() == "привет":
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

    elif user_input.lower() == "пока":
        beta_response = random.choice(responses.BYE_MASSIVE)
        final_response = "До встречи" + beta_response
        return final_response
    elif user_input.lower() == "нормально":
        beta_response = random.choice(responses.NORMALDELA_MASSIVE)
        final_response = "Нормально" + beta_response
        return final_response
    elif user_input.lower() == "как дела":
        beta_response = random.choice(responses.HOWAREYOU_MASSIVE)
        final_response = "Нормально" + beta_response
        return final_response
    elif any(phrase in user_input.lower() for phrase in ["ты талантливый", "ты молодец", "отличная идея", "впечатляет"]):
        beta_response = random.choice(responses.COMPLIMENTS_MASSIVE)
        final_response = beta_response
        return final_response
    elif any(phrase in user_input.lower() for phrase in ["кто ты", "что ты", "ты кто", "что ты такое"]):
        beta_response = random.choice(responses.QUESTION_ABOUT_BOT_MASSIVE)
        final_response = beta_response
        return final_response
    elif any(phrase in user_input.lower() for phrase in ["согласен", "именно так", "так и есть"]):
        beta_response = random.choice(responses.AGREEMENT_MASSIVE)
        final_response = beta_response
        return final_response
    else:
        return "Эх, жаль я не понимаю это. Мой создатель Димон обязательно научит меня и добавит список слов для этого слова!"

def messaging_with_ai():
    print("Познакомьтесь с DimonAI, который всегда рад помочь!")
    while True:
        people_word = input("Вы: ")
        response = generating_response(people_word)
        print("DimonAI: " + response)

if __name__ == "__main__":
    messaging_with_ai()
