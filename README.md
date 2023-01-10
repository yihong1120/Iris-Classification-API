# Flask Server

This repository contains a simple Flask server that exposes three endpoints for handling requests and responses.

## Getting Started

To run the server in this repository, you will need a system with Python and Flask installed.
## Endpoints

* '/key': This endpoint is used to receive JSON data from a client, it generates a random string as a request_id, write the request data and request_id to a file and create a subdirectory in './xy018/json/restore/' with the request_id as the name and write a file with a status of False
* '/return/<key>': This endpoint is used to return the response of the task based on the request_id passed in the key parameter. it reads the inquiry file and check the value of the key, if the value is False, it returns a processing status if the value is False, if the value is True, it returns the content of the response file
* '/request/<key>': This endpoint is used to return the request data based on the request_id passed in the key parameter, it reads the request file and returns its contents

## Scripts

* 'server.py': This script is used to create a Flask server and handle the endpoints.

## Usage
To run the server, navigate to the project directory in your terminal and run the following command:

    python server.py
    
This will start the server on the localhost with the port 8080 and enable the debug mode for development purpose.

## Requirements

* Python 3.x
* Flask
* Flask-Cors

## Note

* The file and folder structure mentioned in the script is just an example and the server will not be able to locate those unless the folder structure exist on the local system.
* The server is running in the debug mode for development purpose only, it's recommended to use a production-ready web server such as Apache or Nginx to serve the application in production.

## Acknowledgements

Thank you to the Python and Flask communities for creating such powerful tools.

## Additional Notes

* The script assumes that the dependencies are installed on the system, you may want to provide the instructions for installing the dependencies in the README.md file
* It also assumes that the endpoint /key is being passed JSON data in the body of the request, it would be useful to mention the format of the data being passed as well as the expected return format.
* Make sure that the server is being run in a secure environment, as it is currently running in debug mode and serving the data over a non-encrypted connection.
* Be sure to configure the correct path on the local system in the script when creating the request_id folder, request file and inquiry file
* You may want to consider adding authentication and authorization to the endpoint to secure the access of the endpoints.
Overall, the script implements a simple Flask web server that exposes three endpoints for handling requests and responses and generating unique request_id. The script provides a simple example of how to implement a RESTful API using the Flask library and can be easily modified to suit different needs.
