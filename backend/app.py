from flask import Flask, request, jsonify
from flask_cors import CORS
import os
from openai import OpenAI
from dotenv import load_dotenv

load_dotenv()  # Load .env variables into the environment

client = OpenAI(
    base_url="https://openrouter.ai/api/v1",
    api_key=os.getenv("OPENROUTER_API_KEY")
)

app = Flask(__name__)
CORS(app)

@app.route('/api/review', methods=['POST'])
def review_code():
    data = request.get_json()

    if not data or 'code' not in data:
        return jsonify({"error": "No code provided"}), 400

    code = data['code']
    prompt = f"Please review the following code and provide constructive feedback:\n\n{code}"

    try:
        response = client.chat.completions.create(
            model="deepseek/deepseek-r1-distill-llama-70b:free",
            messages=[
                {"role": "user", "content": prompt}
            ]
        )

        feedback = response.choices[0].message.content.strip()
        return jsonify({"feedback": feedback})

    except Exception as e:
        error_str = str(e)
        if "code: 408" in error_str or "timeout" in error_str.lower():
            return jsonify({"error": "Server is busy. Please try again after some time."}), 503
        else:
            return jsonify({"error": f"OpenRouter request failed: {error_str}"}), 500

if __name__ == '__main__':
    app.run(debug=True)
