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

    pip install -r requirements.txt

## Running the application

Open another terminal, navigate to the root of the project and run the following command:

    python computation.py

To run the application, navigate to the root of the project and run the following command:

    python app.py

This will start the server on *http://0.0.0.0:8080/* and the application will be ready to handle incoming requests.

## Usage

To use this package, you first need to import it:

    from jsonprocessor import RequestHandler, AlignmentStatus, RequestData

### RequestHandler

The RequestHandler class can be used to write request data to a file and create a subdirectory.

    request_handler = RequestHandler(request_id, request_data)
    request_handler.write_request()
    request_handler.create_subdirectory()

### AlignmentStatus

The AlignmentStatus class can be used to inquire about the status of processed files.

    alignment_status = AlignmentStatus(request_id)
    status = alignment_status.inquire_status()

### RequestData

The RequestData class can be used to get the request data of a processed file.

    request_data = RequestData(request_id)
    data = request_data.get_request()

## Note

* The package is currently only able to handle request and response data as file operations, you can integrate the package with your processing service to make it more useful.
* The package is a simple example and you can modify it to suit your needs.

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

This project is licensed under the [MIT License](https://opensource.org/licenses/MIT)
