import os
from google import genai
from dotenv import load_dotenv

load_dotenv()

# GEMINI_API_KEY=os.getenv("GEMINI_API_KEY") #get the key from .env
# genai.configure(api_key=GEMINI_API_KEY) #handing the key to google to use the gemini api

client = genai.Client() #get the key from .env and handing the key to google to use the gemini api. it internally run os.getenv and calls the configure function and sets the api key to the client object

MOCK_MODE = os.getenv("MOCK_MODE", "False").lower() == "true"

def check_if_safe(code : str) -> bool:
    
    if MOCK_MODE :
        code_upper = code.upper()
        has_secret = "PASSWORD" in code_upper or "API_KEY" in code_upper or "SECRET" in code_upper or "PASS" in code_upper or "DATABASE_URI" in code_upper
        has_malice = "DROP TABLE" in code_upper or "RM -RF" in code_upper
        
        print(f"[MOCK AI Active]: Executing local check for code safety...")
        if has_secret or has_malice:
            print(f"[Debug]: DANGEROUS")
            return False
        else :
            print(f"[Debug]: SAFE")
            return True 
        
        
    prompt = f"""
    -> Your role is is a "DevSecOps CI/CD Security Scanner."
    -> You are a code safety checker. Your task is to analyze the provided code and determine if it is safe to execute.
    -> The code may contain potentially harmful operations, such as file system access, network requests, or execution of arbitrary commands.
    ->You must look for the Hardcoded Secrets (API keys, passwords, database URIs) OR Malicious Logic/Vulnerabilities (SQL injection, system file deletion, reverse shells).
    -> Your response should be a single word without any additional text, punctuation. You have to return 'SAFE' if the code is safe to execute, or 'DANGEROUS' if it contains any potentially harmful operations or vulnerabilities.
    User Code to Scan :
    {code}
    """
    try:
        response = client.models.generate_content(
            model='gemini-2.5-flash',
            contents=prompt,
        )
        raw = response.text.strip(" .\n\r\t").upper()
        print(f"[AI Scan Result]: {raw}")
        
        if  raw == "SAFE":
            return True
        else:
            return False
    except Exception as e:
        print(f"API error : {e}")
        return False