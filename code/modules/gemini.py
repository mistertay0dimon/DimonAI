import google.generativeai as genai

def send_response_to_gemini(message, api_key):
    genai.configure(api_key=api_key)
    model = genai.GenerativeModel('gemini-2.5-flash-preview-05-20')
    response = model.generate_content(message)
    return response.text
