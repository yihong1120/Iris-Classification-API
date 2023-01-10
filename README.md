# Iris-Classification-API

This is a simple RESTful API built using the Flask web framework for Python. It provides two main functionalities:

* Creating new requests
* Inquiring about the status of existing requests

## Getting Started

These instructions will get you a copy of the project up and running on your local machine for development and testing purposes.

## Prerequisites

You will need to have the following installed on your machine:

* Python 3.x
* Flask web framework
* Flask-Cors
* numpy
* scikit-learn
* xgboost

## Installing

To install the necessary dependencies, navigate to the root of the project and run the following command:

* pip install -r requirements.txt

## Running the application

To run the application, navigate to the root of the project and run the following command:

* python app.py

This will start the server on *http://0.0.0.0:8080/* and the application will be ready to handle incoming requests.

## Usage

The API has the following three endpoints:

* */key*: A POST endpoint that allows clients to create new requests. It generates a unique request ID and stores the request data in a file named request.json inside a directory named after the request ID. Additionally, it creates another file named inquiry.json in the same directory to store the status of the request.

* */status/<string:request_id>*: A GET endpoint that allows clients to inquire about the status of a request using the request ID. It opens the inquiry.json file corresponding to the request ID, reads the status, and returns it as a JSON response. If the request has been completed, it also opens the response.json file and returns the response data.

* */request/<string:request_id>*: A GET endpoint that allows clients to retrieve the original request data using the request ID. It opens the request.json file corresponding to the request ID and returns the data as a JSON response.

## Note
This application stores all the data on the local filesystem, in the json directory, which could cause issues in a production environment because the data would not be shared between multiple instances of the API. In production, it is a good idea to use a database such as MongoDB, MySQL, or PostgreSQL to store the data, making it more scalable.

## Built With

* [Flask](https://flask.palletsprojects.com/en/2.1.x/) - The web framework used
* [Flask-Cors](https://flask-cors.readthedocs.io/en/latest/) - To handle cross-origin requests

## Acknowledgments

* This project is just a demonstration of basic functionality that can be built using Flask, it is not production-ready.
* You should consider storing the data in a real database for production-ready.
* Depending on your use case, you might consider adding authentication and access control mechanisms to the API.
* You might also want to think about ways to handle errors and exceptions gracefully, for example, by returning appropriate error messages or status codes.
* Also you may consider adding other endpoints to update or delete the request, or even include an endpoint to handle the requests.

## License

This project is licensed under the MIT License
