# Flask Application for CRUD Operations on MongoDB

This project is a Flask application that allows users to perform CRUD (Create, Read, Update, Delete) operations on a MongoDB database for a User resource using a REST API. The REST API endpoints can be accessed via HTTP requests and can be tested using Postman.

## Requirements

To run this application, you will need:

- Python 3.6 or higher
- Flask
- pymongo
- Flask-PyMongo
- Postman (for testing)

## Installation

1. Clone the repository: `git clone https://github.com/djharshit/flask-api-server`
2. Navigate to the project directory: `cd flask-api-server`
3. Create a virtual environment: `python3 -m venv env`
4. Activate the virtual environment: `source env/bin/activate`
5. Install the required packages: `pip install -r requirements.txt`
6. Change the MongoDB connection string in `app.py` to your own connection string
7. Start the application: `python app.py`

## Usage

Once the application is running, you can access the REST API endpoints using Postman or any other HTTP client.

The available endpoints are:

- GET `/users`: Returns a list of all users
- GET `/users/<user_id>`: Returns a specific user
- POST `/users`: Creates a new user
- PUT `/users/<user_id>`: Updates a specific user
- DELETE `/users/<user_id>`: Deletes a specific user
