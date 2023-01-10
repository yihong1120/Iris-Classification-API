import requests
import json
import os
import time

# Read data from a JSON file at the specified path
def read_json(file_path: str):
    with open(file_path, "r") as f:
        return json.load(f)

# Write data to a JSON file at the specified path
def write_json(file_path: str, data):
    with open(file_path, 'w') as f:
        json.dump(data, f)

# Send a request for each JSON file in the specified directory, and write the requestId from the response to a specified output file
def send_requests(input_dir: str, output_file: str):
    # Dictionary to store requestIds
    request_ids = {}

    # URL for the server
    create_requestID_url = "http://192.168.0.1:8080/key"

    # Sort JSON filenames alphabetically
    sorted_files = sorted(os.listdir(input_dir))

    # Iterate through JSON files
    for file in sorted_files:
        # Read data from JSON file
        data = read_json(os.path.join(input_dir, file))

        # Send request to server
        response = requests.post(create_requestID_url, json=data)

        # Check if request was successful
        if response.status_code == 200:
            # Get requestId from response
            request_id = response.json()["requestId"]
            print(f"{file}: {request_id}")

            # Add requestId to dictionary
            request_ids[file] = request_id
        else:
            print("An error occurred.")

    # Write dictionary to output JSON file
    write_json(output_file, request_ids)

# Send a request to the server for each request ID in a specified input file, and write the server's response to a specified output file
def get_responses(input_file: str, output_dir:str):
    # Read request IDs from input file
    request_ids = read_json(input_file)

    # Iterate through request IDs
    for file, request_id in request_ids.items():
        # Build URL for request
        response_url = f"http://192.168.0.1:8080/return/{request_id}"
        request_url = f"http://192.168.0.1:8080/request/{request_id}"

        # Create a subdirectory to store the response and request data
        save_folder = file.split(".")[0]
        path_to_save = os.path.join(output_dir, save_folder)
        if not os.path.exists(path_to_save):
            os.makedirs(path_to_save)

        # Send request to server
        response = requests.get(response_url)

        # Check if status was still processing
        while response.json()["status"] == "PROCESSING":
            # Check if request was successful
            if response.status_code == 200:
                time.sleep(1)
                response = requests.get(response_url)
        
        print(f"{file} is finished computating.")

        # Save the response data in a JSON file
        save_response_path = os.path.join(path_to_save , "response.json")
        write_json(save_response_path, response.json())

        # Save the request data in a JSON file
        request = requests.get(request_url)
        save_request_path = os.path.join(path_to_save, "request.json")
        write_json(save_request_path, request.json())
       
if __name__ == "main":
    input_dir = "route/your_json_input"
    output_dir = "route/your_json_output"
    request_ids_file = os.path.join(output_dir, "request_ids.json")
    
    # Send requests for each JSON file in the input_dir directory and write the requestIds to the request_ids_file
    send_requests(input_dir, request_ids_file)

    # Send requests for each request ID in the path_index_json file and write the responses to the output_json file
    get_responses(request_ids_file, output_dir)
