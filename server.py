"""This module is used to create a REST API using Flask and MongoDB"""

# Importing the required libraries
from datetime import datetime
from os import environ
from typing import Optional

from flask import Flask, jsonify, render_template, request

from api import Connection

# Variables
HOST: str = environ.get("MONGO_URI", "")
PORT: int = int(environ.get("PORT", 5000))

client: Connection = Connection(host=HOST)

if not client.is_connected:
    print("Could not connect to the database")
    exit(1)

# Creating the Flask app
app = Flask(__name__)


@app.route("/")
def home_page():
    """
    Home page for documentation of the API
    """
    return render_template("index.html")


@app.route("/users", methods=["GET", "POST"])  # type: ignore
def func1():
    """Function to handle GET and POST requests on /users route"""
    if request.method == "GET":
        print(client.get_all_document())
        return jsonify(
            {"Datetime": datetime.now(), "AllUsers": client.get_all_document()}
        )

    elif request.method == "POST":
        name: Optional[str] = request.form.get("name")
        email: Optional[str] = request.form.get("email")
        password: Optional[str] = request.form.get("password")

        if not name or not email or not password:
            return (
                jsonify(
                    {
                        "Datetime": datetime.now(),
                        "Error": "Please provide all the fields",
                    }
                ),
                400,
            )

        x: bool = client.insert_in_collection(
            {"name": name, "email": email, "password": password}
        )

        return jsonify({"Datetime": datetime.now(), "Succeed": x})


@app.route("/users/<string:doc_id>", methods=["GET", "PUT", "DELETE"])  # type: ignore
def func2(doc_id: str):
    """Function to handle GET, PUT and DELETE requests on /users/<string:doc_id> route"""
    if request.method == "GET":
        return jsonify(
            {"Datetime": datetime.now(), "User": client.get_one_document(doc_id)}
        )

    elif request.method == "PUT":
        name: str = request.form.get("name", "")
        email: str = request.form.get("email", "")
        password: str = request.form.get("password", "")

        _: bool = client.update_one_document(
            doc_id, {"name": name, "email": email, "password": password}
        )
        return jsonify({"Datetime": datetime.now(), "Updated": _})

    elif request.method == "DELETE":
        _ = client.delete_one_document(doc_id)
        return jsonify({"Datetime": datetime.now(), "Deleted": _})


if __name__ == "__main__":
    print("[+] Connecting to the database...")
    app.run(host="0.0.0.0", port=PORT, debug=True)
