import os
import time
import shutil
import json
from collections import OrderedDict
from typing import Any
import pickle

# Function to extract data from a JSON file
def get_json_data(json_path:str) -> Any:
    with open(json_path, "r") as f:
        return json.load(f, object_pairs_hook=OrderedDict)

# Function to write data to a JSON file
def write_json_file(path: str, data: Any) -> None:
    with open(path, 'w') as f:
        json.dump(data, f)

# Function to remove folders that exist over 30 days
def delete_old_folders(dir_path: str) -> None:
    # Get the current time in seconds since the epoch
    current_time = time.time()

    # Iterate through all the folders in the given directory
    for folder in os.listdir(dir_path):
        # Get the full path of the folder
        folder_path = os.path.join(dir_path, folder)
        # Check if the path is a directory
        if os.path.isdir(folder_path):
            # Get the creation time of the folder in seconds since the epoch
            creation_time = os.path.getctime(folder_path)
            # Calculate the difference in time between the current time and the creation time
            time_diff = current_time - creation_time
            # If the difference is greater than 30 days (in seconds), delete the folder
            if time_diff > 2592000:
                os.rmdir(folder_path)

# load model
with open('./model/iris.pickle', 'rb') as f:
    xgboostModel = pickle.load(f)

# write the model into function
def predict(input):
    input = get_json_data(input)
    pred=xgboostModel.predict(input)[0]
    return pred

# Set the paths for the directories where the JSON files are stored
work_path = "xy018/json/new_work/"
restore_path = "xy018/json/restore/"

# Loop indefinitely
while True:
    try:
        # Delete the data which has been posted over 30 days
        delete_old_folders(restore_path)
        # Get a sorted list of all JSON files in the "new_work" directory
        sorted_json_files = sorted(os.listdir(work_path))

        # If there are any JSON files in the directory
        if sorted_json_files:
            # Process each file in the list
            for file in sorted_json_files:
                # Extract the request ID from the filename
                request_id = file.split(".")[0]
                print(f"Commencing alignment, request ID: {request_id}")
                time_start = time.time()

                # Wait 10 seconds to ensure the file has finished writing
                time.sleep(10)

                # Run the iris prediction function on the file
                predict(os.path.join(restore_path, file))

                # Move the processed file from the "new_work" directory to the "restore" directory
                shutil.move(os.path.join(work_path, file), os.path.join(restore_path, request_id, "request.json"))

                # Add the request ID to the aligned JSON file
                alignment_json_path = os.path.join(restore_path, request_id, "response.json")
                alignment_json = get_json_data(alignment_json_path)
                alignment_json["requestId"] = request_id
                write_json_file(alignment_json_path, alignment_json)

                # Edit the status to the inquiry JSON file
                inquiry_path = os.path.join(restore_path, request_id, "inquiry.json")
                write_json_file(inquiry_path, {request_id: True})

                time_end = time.time()
                print(f"Finished alignment, request ID: {request_id}")
                print(f"Time consuming: {time_end - time_start} seconds")
    except Exception as e:  # Catch any errors that might occur and print the error message
        print(f"Error: {e}")
