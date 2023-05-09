"""This module is used to create a REST API using Flask and MongoDB"""

from datetime import datetime
import argparse
import bson
import pymongo
from flask import Flask, jsonify, request


class Connection:
    """This class is used to connect to the database and perform operations on it
    """

    def __init__(self, host: str) -> None:
        """This constructor is used to connect to the database and get the collection

        Args:
            host (str): The host address of the database
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


@app.route('/users', methods=['GET', 'POST'])
def func1():
    """Function to handle GET and POST requests on /users route
    """
    if request.method == 'GET':
        all_data = client.get_all_document()
        result = jsonify({
            'Datetime': datetime.now(),
            'AllUsers': list(all_data)
        })

    elif request.method == 'POST':
        document = {
            'name': request.form.get('name'),
            'email': request.form.get('email'),
            'password': request.form.get('password')
        }
        x = client.insert_in_collection(document)

        result = jsonify({
            'Datetime': datetime.now(),
            'Succeed': x
        })

    return result


@app.route('/users/<string:doc_id>', methods=['GET', 'PUT', 'DELETE'])
def func2(doc_id: str):
    """Function to handle GET, PUT and DELETE requests on /users/<string:doc_id> route
    """
    if request.method == 'GET':
        x = client.get_one_document(doc_id)
        result = {
            'Datetime': datetime.now(),
            'User': x
        }

    elif request.method == 'PUT':
        x = client.update_one_document(doc_id, request.form)
        result = {
            'Datetime': datetime.now(),
            'Updated': x
        }

    elif request.method == 'DELETE':
        x = client.delete_one_document(doc_id)
        result = {
            'Datetime': datetime.now(),
            'Deleted': x
        }

    return jsonify(result)


parser = argparse.ArgumentParser()
parser.add_argument('--host', type=str, default='mongodb://127.0.0.1:27017/',
                    required=False, help='The host address of the database')

if __name__ == '__main__':
    args = parser.parse_args()
    print('Connecting to the database...')
    client = Connection(host=args.host)

    if client.is_connected():
        print('Connected to the database')
        app.run(host='0.0.0.0', port=5000, debug=True)
        client.close_connection()

    else:
        print('Could not connect to the database')
