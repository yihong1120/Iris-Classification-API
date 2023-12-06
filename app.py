import os
import json
import time
import string
import random

from flask import Flask, request, jsonify
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

class RequestHandler:
    def __init__(self, request_id: str, request_data: dict):
        self.request_id = request_id
        self.request_data = request_data
        self.work_path = "./xy018/json/new_work/"
        self.restore_path = "./xy018/json/restore/"

    def write_request(self):
        """Write request data to a file"""
        with open(f'{self.work_path}{self.request_id}.json', 'w') as f:
            json.dump(self.request_data, f)

    def create_subdirectory(self):
        """Create a subdirectory and write a file with a status of False"""
        os.makedirs(f'{self.restore_path}{self.request_id}', exist_ok=True)
        with open(f'{self.restore_path}{self.request_id}/inquiry.json', 'w') as f:
            json.dump({self.request_id:False}, f)

class PredictionStatus:
    def init(self, request_id: str):
        self.request_id = request_id
        self.restore_path = "./xy018/json/restore/"
            
    def inquire_status(self):
        """Read the inquiry file and check the value of the key"""
        with open(f'{self.restore_path}{self.request_id}/inquiry.json', 'r') as f:
            inquiry = json.load(f)
        if not inquiry[self.request_id]:
            """Return a processing status if the value is False"""
            return jsonify({"requestId": self.request_id, "status": "PROCESSING"})
            
        """Read the response file and return its contents if the value is True"""
        with open(f'{self.restore_path}{self.request_id}/response.json', 'r') as f:
            response = json.load(f)
        return jsonify(response)

class RequestData:
    def init(self, request_id: str):
        self.request_id = request_id
        self.restore_path = "./xy018/json/restore/"
        
    def get_request(self):
        """Read the request file and return its contents"""
        with open(f'{self.restore_path}{self.request_id}/request.json', 'r') as f:
            request = json.load(f)
        return jsonify(request)

@app.route('/key', methods=['POST'])
def create_key():
    # Generate request_id
    timestamp = str(int(time.time() * 1000000))
    random_string = ''.join(random.choices(string.ascii_letters + string.digits, k=10))
    request_id = f'{timestamp}{random_string}'
    # Receive json data from the user
    request_data = request.get_json()

    # Create an instance of the RequestHandler class and call its methods
    request_handler = RequestHandler(request_id, request_data)
    request_handler.write_request()
    request_handler.create_subdirectory()

    return jsonify({"requestId": request_id, "status": "PROCESSING"})
    
@app.route('/return/<key>', methods=['GET'])
def inquire_prediction_status(key):
    # Create an instance of the PredictionStatus class and call its method
    prediction_status = PredictionStatus(key)
    return prediction_status.inquire_status()

@app.route('/request/<key>', methods=['GET'])
def request_orgine_data(key):
    # Create an instance of the RequestData class and call its method
    request_data = RequestData(key)
    return request_data.get_request()

if __name__ == "__main__":
    app.run()
