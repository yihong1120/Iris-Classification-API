import os
import time
import shutil
import json
import pickle

class JSONHandler:
    @staticmethod
    def get_data(json_path: str):
        """
        Reads data from a json file and returns it as a dictionary
        :param json_path: path to json file
        :return: data in json file as a dictionary
        """
        try:
            with open(json_path, "r") as f:
                return json.load(f)
        except Exception as e:
            print(f"Error reading JSON file: {e}")

    @staticmethod
    def write_data(path: str, data: dict):
        """
        Writes data to a json file
        :param path: path to json file
        :param data: data to be written in the json file
        """
        try:
            with open(path, 'w') as f:
                json.dump(data, f)
        except Exception as e:
            print(f"Error writing JSON file: {e}")

class FolderHandler:
    @staticmethod
    def delete_old(dir_path: str):
        """
        Deletes folders that are older than 30 days
        :param dir_path: path to the directory containing the folders
        """
        try:
            current_time = time.time()
            for folder in os.listdir(dir_path):
                folder_path = os.path.join(dir_path, folder)
                if os.path.isdir(folder_path):
                    creation_time = os.path.getctime(folder_path)
                    time_diff = current_time - creation_time
                    if time_diff > 2592000:
                        shutil.rmtree(folder_path)
        except Exception as e:
            print(f"Error deleting old folders: {e}")

class ModelHandler:
    def __init__(self):
        """
        loads a machine learning model from a pickle file
        """
        try:
            with open('./model/iris.pickle', 'rb') as f:
                self.xgboostModel = pickle.load(f)
        except Exception as e:
            print(f"Error loading model: {e}")

    def predict(self, input_json: str):
        """
        makes predictions using the loaded model
        :param input_json: path to json file with input data
        :return: prediction result
        """
        try:
            input_data = JSONHandler.get_data(input_json)
            pred = self.xgboostModel.predict(input_data)[0]
            return pred
        except Exception as e:
            print(f"Error predicting: {e}")

class WorkflowHandler:
    def __init__(self):
        """
        initializes the paths to the work and restore folders
        """
        self.work_path = "xy018/json/new_work/"
        self.restore_path = "xy018/json/restore/"

    def run(self):
        """
        runs the workflow, which includes:
        1. Deletes old folders from the restore path
        2. Sorts the json files in the work path
        3. For each file in the work path:
            - Extracts the request ID from the file name
            - Prints a message indicating the start of prediction for the request
            - Sleeps for 10 seconds
            - Makes a prediction using the loaded model and input data from the json file
            - If the prediction is successful, prints the prediction result
            - If the prediction fails, prints an error message and skips the file
            - Creates a new folder in the restore path with the request ID as the name
            - Moves the json file to the new folder and renames it as "request.json"
            - Writes the prediction result and request ID to a json file in the new folder and names it "response.json"
            - Writes a json file in the new folder named "inquiry.json" with the request ID and a value of true
            - Prints a message indicating the end of prediction for the request and the time consumed
        4. Repeats the process in an infinite while loop
        """
        while True:
            FolderHandler.delete_old(self.restore_path)
            sorted_json_files = sorted(os.listdir(self.work_path))
            for file in sorted_json_files:
                request_id = file.split(".")[0]
                print(f"Commencing prediction, request ID: {request_id}")
                time_start = time.time()
                time.sleep(10)
                prediction_result = ModelHandler().predict(os.path.join(self.work_path, file))
                if prediction_result:
                    print(f"Prediction result: {prediction_result}")
                else:
                    print("Error making prediction, skipping file...")
                    continue
                os.makedirs(os.path.join(self.restore_path, request_id), exist_ok=True)
                shutil.move(os.path.join(self.work_path, file), os.path.join(self.restore_path, request_id, "request.json"))
                response_json_path = os.path.join(self.restore_path, request_id, "response.json")
                JSONHandler.write_data(response_json_path, {"requestId": request_id, "prediction_result": prediction_result})
                inquiry_path = os.path.join(self.restore_path, request_id, "inquiry.json")
                JSONHandler.write_data(inquiry_path, {request_id: True})
                time_end = time.time()
                print(f"Finished prediction, request ID: {request_id}")
                print(f"Time consuming: {time_end - time_start} seconds")

if __name__ == "__main__":
    handler = WorkflowHandler()
    handler.run()
