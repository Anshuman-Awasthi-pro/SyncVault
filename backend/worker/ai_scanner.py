import os
import google.generativeai as genai
from dotenv import load_dotenv

load_dotenv()

GEMINI_API_KEY=os.getenv("GEMINI_API_KEY") #get the key from .env
genai.configure(api_key=GEMINI_API_KEY) #handing the key to google to use the gemini api
model = genai.GenerativeModel('gemini-1.5-flash')

def check_if_safe(code : str) -> bool:
    prompt = f"""
    -> Your role is is a "DevSecOps CI/CD Security Scanner."
    -> You are a code safety checker. Your task is to analyze the provided code and determine if it is safe to execute.
    -> The code may contain potentially harmful operations, such as file system access, network requests, or execution of arbitrary commands.
    ->You must look for the Hardcoded Secrets (API keys, passwords, database URIs) AND Malicious Logic/Vulnerabilities (SQL injection, system file deletion, reverse shells).
    -> Your response should be a simple. You have to return 'SAFE' if the code is safe to execute, or 'UNSAFE' if it contains any potentially harmful operations or vulnerabilities.
    User Code to Scan :
    {code}
    """
    try:
        response = model.generate_content(prompt)
        if "SAFE" in response.text.strip().upper() :
            return True
        else:
            return False
    except Exception as e:
        print(f"API error : {e}")
        return False