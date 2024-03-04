"""This module is used to create a REST API using Flask and MongoDB"""

import argparse
from datetime import datetime

import bson
import pymongo
from flask import Flask
from flask_restful import Api, Resource, reqparse


class Connection:
    """This class is used to connect to the database and perform operations on it
    """

    def __init__(self, host: str) -> None:
        """This constructor is used to connect to the database and get the collection
        """
        self.__my_client = pymongo.MongoClient(
            host=host)
        self.__my_db = self.__my_client.get_database('data')
        self.my_collection = self.__my_db.get_collection('identity')

    def get_all_document(self) -> list:
        """Gets all the documents from the collection

        Returns:
            list: A list of all the documents
        """
        for i in self.my_collection.find():
            i['_id'] = str(i['_id'])  # Convert ObjectId to string
            yield i

    def get_one_document(self, doc_id: str) -> dict:
        """Returns a document from the collection

        Args:
            doc_id (str): The doc_id of the document to be returned

        Returns:
            dict: The document
        """

        try:
            x = self.my_collection.find_one({'_id': bson.ObjectId(doc_id)})
            x['_id'] = str(x['_id'])  # Convert ObjectId to string
            return x

        except bson.errors.InvalidId:
            return None

    def insert_in_collection(self, document: dict) -> bool:
        """Inserts a document in the collection

        Args:
            document (dict): A dictionary containing the document to be inserted

        Returns:
            bool: Returns True if the document is inserted successfully, else False
        """

        name = document.get('name')
        email = document.get('email')
        password = document.get('password')

        x = self.my_collection.insert_one({
            'name': name,
            'email': email,
            'password': password
        })

        return x.acknowledged

    def delete_one_document(self, doc_id: str) -> bool:
        """Deletes a document from the collection

        Args:
            doc_id (str): The doc_id of the document to be deleted

        Returns:
            bool: Returns True if the document is deleted successfully, else False
        """
        try:
            x = self.my_collection.delete_one({'_id': bson.ObjectId(doc_id)})
            return x.acknowledged

        except bson.errors.InvalidId:
            return False

    def update_one_document(self, doc_id: str, document: dict) -> bool:
        """Updates a document in the collection

        Args:
            doc_id (str): The doc_id of the document to be updated
            document (dict): A dictionary containing the updated document

        Returns:
            bool: Returns True if the document is updated successfully, else False
        """
        try:
            x = self.my_collection.update_one(
                {'_id': bson.ObjectId(doc_id)}, {'$set': document})
            return x.acknowledged

        except bson.errors.InvalidId:
            return False

    def is_connected(self) -> bool:
        """Checks if the connection is established or not

        Returns:
            bool: Returns True if the connection is established, else False
        """
        try:
            self.__my_client.server_info()
            return True

        except pymongo.errors.ServerSelectionTimeoutError:
            return False

    def close_connection(self):
        """Closes the connection with the database
        """
        self.__my_client.close()


app = Flask(__name__)
api = Api(app)

helloworld_parser = reqparse.RequestParser()
helloworld_parser.add_argument(
    'name', type=str, help='Name of the person', location='form', required=True)
helloworld_parser.add_argument(
    'email', type=str, help='Email of the person', location='form', required=True)
helloworld_parser.add_argument(
    'password', type=str, help='Password of the person', location='form', required=True)

arg_parser = argparse.ArgumentParser()
arg_parser.add_argument('--host', type=str, default='mongodb://127.0.0.1:27017/',
                        required=False, help='The host address of the database')


class UserOne(Resource):
    """
    Class for /users endpoint of the API with GET and POST methods
    """

    def get(self):
        """
        The GET method for /users endpoint of the API
        """
        all_users = client.get_all_document()
        return {
            'Date': str(datetime.now()),
            'AllUsers': list(all_users)
        }

    def post(self):
        """
        The POST method for /users endpoint of the API
        """
        req_args = helloworld_parser.parse_args()

        document = {
            'name': req_args.get('name'),
            'email': req_args.get('email'),
            'password': req_args.get('password')
        }
        x = client.insert_in_collection(document)

        return {
            'Date': str(datetime.now()),
            'Succeed': x
        }


class UserTwo(Resource):
    """
    Class for /users/<string:doc_id> endpoint of the API with GET, PUT and DELETE methods
    """

    def get(self, doc_id):
        """
        The GET method for /users/<string:doc_id> endpoint of the API
        """
        x = client.get_one_document(doc_id)
        return {
            'Date': str(datetime.now()),
            'User': x
        }

    def put(self, doc_id):
        """
        The PUT method for /users/<string:doc_id> endpoint of the API
        """
        req_args = helloworld_parser.parse_args()

        document = {
            'name': req_args.get('name'),
            'email': req_args.get('email'),
            'password': req_args.get('password')
        }
        x = client.update_one_document(doc_id, document)

        return {
            'Date': str(datetime.now()),
            'Succeed': x
        }

    def delete(self, doc_id):
        """
        The DELETE method for /users/<string:doc_id> endpoint of the API
        """
        x = client.delete_one_document(doc_id)
        return {
            'Date': str(datetime.now()),
            'Succeed': x
        }


api.add_resource(UserOne, '/users')
api.add_resource(UserTwo, '/users/<string:doc_id>')

if __name__ == '__main__':
    cmd_args = arg_parser.parse_args()
    print('Connecting to the database...')
    client = Connection(host=cmd_args.host)

    if client.is_connected():
        print('Connected to the database')
        app.run(host='0.0.0.0', port=5000, debug=True)
        client.close_connection()

    else:
        print('Could not connect to the database')
