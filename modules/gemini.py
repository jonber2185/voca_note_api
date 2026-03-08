import os
import json
from google import genai
from google.genai import types
from dotenv import load_dotenv
load_dotenv()


client = genai.Client(api_key=os.getenv("GEMINI_API_KEY"))

def load_prompt(filename):
    path = os.path.join(os.path.dirname(__file__), '..', 'prompts', filename)
    with open(path, 'r', encoding='utf-8') as f:
        return f.read()

def get_gemini_response(words: list) -> dict:
    system_instruction = load_prompt('gemini_system.txt')

    response = client.models.generate_content(
        model="gemini-2.5-flash", 
        contents=str(words),
        config=types.GenerateContentConfig(
            system_instruction=system_instruction,
            response_mime_type="application/json",
            max_output_tokens=8000,
        )
    )
    res_text = response.text.strip()
    
    if res_text.startswith("```json"):
        res_text = res_text[7:] # 앞의 ```json 제거
    if res_text.endswith("```"):
        res_text = res_text[:-3] # 뒤의 ``` 제거
        
    res_text = res_text.strip() # 남은 공백 제거
    
    try:
        return json.loads(res_text)
    except json.JSONDecodeError as e:
        print(f"JSON Parsing Error: {e}")
        print(f"Raw Response: {res_text}")
        raise e
