
from flask import Flask, request, jsonify
import secrets

app = Flask(__name__)

# Generate three unique API keys
API_KEYS = {
    secrets.token_hex(16): "Consumer 1",
    secrets.token_hex(16): "Consumer 2",
    secrets.token_hex(16): "Consumer 3"
}

# Display generated keys in the terminal
print("Generated API Keys:")
for key, consumer in API_KEYS.items():
    print(consumer, ":", key)


@app.route("/")
def home():
    return "Text Processing API is Running!"


@app.route("/process", methods=["POST"])
def process_text():

    # Get API key from request header
    api_key = request.headers.get("X-API-Key")

    # Validate API key
    if api_key not in API_KEYS:
        return jsonify({
            "error": "Invalid or missing API key"
        }), 401

    # Get text from JSON body
    data = request.get_json()

    if not data or not isinstance(data.get("text"), str):
        return jsonify({
            "error": "Please provide text in JSON format"
        }), 400

    text = data["text"]

    # Process text into uppercase
    processed_text = text.upper()

    return jsonify({
        "consumer": API_KEYS[api_key],
        "original_text": text,
        "processed_text": processed_text,
        "message": "Text processed successfully!"
    }), 200


if __name__ == "__main__":
    app.run(debug=True)
