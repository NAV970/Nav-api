from flask import Flask, request, jsonify
import requests
import os

app = Flask(__name__)

OPENROUTER_API_KEY = os.getenv("OPENROUTER_API_KEY")

@app.route("/ai/ask", methods=["GET"])
def ask_ai():
    question = request.args.get("question")

    if not question:
        return jsonify({"error": "question parameter required"}), 400

    try:
        response = requests.post(
            "https://openrouter.ai/api/v1/chat/completions",
            headers={
                "Authorization": f"Bearer {OPENROUTER_API_KEY}",
                "Content-Type": "application/json"
            },
            json={
                "model": "meta-llama/llama-3.3-70b-instruct:free",
                "messages": [
                    {
                        "role": "user",
                        "content": question
                    }
                ]
            },
            timeout=60
        )

        data = response.json()

        reply = data["choices"][0]["message"]["content"]

        return jsonify({
            "reply": reply
        })

    except Exception as e:
        return jsonify({
            "error": str(e)
        }), 500

if __name__ == "__main__":
    app.run()
