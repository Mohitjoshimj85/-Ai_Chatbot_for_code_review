from flask import Flask, request, jsonify
from openai import OpenAI
from flask_cors import CORS
import json
import os
from dotenv import load_dotenv

load_dotenv()

app = Flask(__name__)
CORS(app)

client = OpenAI(
    base_url="https://openrouter.ai/api/v1",
    api_key=os.getenv("OPENROUTER_API_KEY"),
)

@app.route('/api/review', methods=['POST'])
def review_code():
    data = request.get_json()

    if not data or 'code' not in data:
        return jsonify({"error": "No code provided"}), 400

    code = data['code']

    prompt = f"""
    Review the following code and respond ONLY in JSON with this structure:
    {{
        "summary": "Brief overview of the code",
        "bugs": "List of any bugs or issues found",
        "suggestions": "Improvements or best practices suggestions"
    }}

    Code:
    {code}
    """

    try:
        response = client.chat.completions.create(
            model="deepseek/deepseek-r1-distill-llama-70b:free",
            messages=[{"role": "user", "content": prompt}]
        )

        raw_reply = response.choices[0].message.content.strip()

        # Remove ```json ... ``` or ``` wrappers if present
        if raw_reply.startswith("```"):
            raw_reply = raw_reply.strip("`")
            if raw_reply.lower().startswith("json"):
                raw_reply = raw_reply[4:].strip()
        
        # Try parsing JSON
        try:
            parsed = json.loads(raw_reply)
        except json.JSONDecodeError:
            parsed = {
                "summary": raw_reply,
                "bugs": "Could not parse JSON.",
                "suggestions": ""
            }


        return jsonify(parsed)

    except Exception as e:
        err = str(e)
        if "408" in err:
            return jsonify({"error": "Server is busy, please try again later."}), 503
        return jsonify({"error": f"OpenRouter request failed: {err}"}), 500

if __name__ == '__main__':
    app.run(debug=True)
