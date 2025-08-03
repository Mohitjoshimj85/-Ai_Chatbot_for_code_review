import os
import json
import re
from openai import OpenAI
from dotenv import load_dotenv

load_dotenv()

api_key = os.getenv("OPENAI_API_KEY")
if not api_key:
    raise ValueError("OPENAI_API_KEY not found in .env")

client = OpenAI(api_key=api_key)

def extract_json(text):
    """
    Extract JSON from GPT response, even if it's wrapped in markdown or has extra text.
    """
    try:
        # Match JSON enclosed in ```json ... ```
        match = re.search(r"```json\s*(\{.*?\})\s*```", text, re.DOTALL)
        if match:
            return json.loads(match.group(1))
        
        # Match raw JSON in entire string
        match = re.search(r"(\{.*?\})", text, re.DOTALL)
        if match:
            return json.loads(match.group(1))

        raise ValueError("No JSON object could be extracted.")

    except json.JSONDecodeError as e:
        raise ValueError(f"JSON decode failed: {str(e)}")

def analyze_code(code, language):
    try:
        prompt = f"""
You are an expert code reviewer.
Analyze the following {language} code:
-----
{code}
-----
Return the result as a JSON object with the following fields:
- summary: A brief explanation of what the code does.
- bugs: A list of bugs or potential issues (if any).
- suggestions: Improvements for performance, security, or readability.

Only return raw JSON. No extra text.
"""

        response = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": "You are a helpful and concise code review expert."},
                {"role": "user", "content": prompt}
            ],
            temperature=0.3,
            max_tokens=700
        )

        reply = response.choices[0].message.content
        print("🔹 Raw GPT Response:", reply)

        parsed_json = extract_json(reply)
        return parsed_json

    except Exception as e:
        print("❌ analyze_code failed:", str(e))
        return {
            "summary": "Error: Could not analyze the code.",
            "bugs": [str(e)],
            "suggestions": []
        }
