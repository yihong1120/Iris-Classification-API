import os
import json
import time
import string
import random

from flask import Flask, request, jsonify
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

def generate_random_string() -> str:
    """Generate a random string of length 10."""
    return ''.join(random.choices(string.ascii_letters + string.digits, k=10))

@app.route('/key', methods=['POST'])
def create_key():
    # Generate request_id
    timestamp = str(int(time.time() * 1000000))
    random_string = generate_random_string()
    request_id = f'{timestamp}{random_string}'
    # Receive json data from the user
    request_data = request.get_json()

    # Write request data to a file
    with open(f'./xy018/json/new_work/{request_id}.json', 'w') as f:
        json.dump(request_data, f)

    # Create a subdirectory and write a file with a status of False
    os.makedirs(f'./xy018/json/restore/{request_id}', exist_ok=True)
    with open(f'./xy018/json/restore/{request_id}/inquiry.json', 'w') as f:
        json.dump({request_id: False}, f)

    return jsonify({"requestId": request_id, "status": "PROCESSING"})

@app.route('/return', methods=['GET'])
def inquire_alignment_status(key):
    # Read the inquiry file and check the value of the key
    with open(f'./xy018/json/restore/{key}/inquiry.json', 'r') as f:
        inquiry = json.load(f)
    if not inquiry[key]:
        # Return a processing status if the value is False
        return jsonify({"requestId": key, "status": "PROCESSING"})

    # Read the response file and return its contents if the value is True
    with open(f'./xy018/json/restore/{key}/response.json', 'r') as f:
        response = json.load(f)
    return jsonify(response)

@app.route('/request', methods=['GET'])
def request_orgine_data(key):
    # Read the request file and return its contents
    with open(f'./xy018/json/restore/{key}/request.json', 'r') as f:
        request = json.load(f)
    return jsonify(request)

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=8080, debug=True)
