from flask import Flask, render_template, request, redirect, jsonify
import pymongo
from datetime import datetime


class Connection:
    def __init__(self) -> None:
        self.__myClient = pymongo.MongoClient(
            host='mongodb://127.0.0.1:27017/')
        self.__myDB = self.__myClient.get_database('data')
        self.myCollection = self.__myDB.get_collection('identity')

    def get_all_document(self) -> list:
        for i in self.myCollection.find():
            i['_id'] = str(i['_id'])
            yield i

    def insert_in_collection(self, document: dict) -> bool:
        name = document.get('name')
        email = document.get('email')
        password = document.get('password')

        x = self.myCollection.insert_one({
            'name': name,
            'email': email,
            'password': password
        })

        return x.acknowledged

    def is_connected(self):
        try:
            self.__myClient.get_database('data')
            return True

        except:
            return False

    def close_connection(self):
        self.__myClient.close()


app = Flask(__name__)


@app.route('/users', methods=['GET', 'POST'])
def func1():
    if request.method == 'GET':
        all_data = client.get_all_document()
        result = jsonify({
            'Datetime': datetime.now(),
            'AllUsers': [i for i in all_data]
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

@app.route('/users/<string:id>', methods=['GET', 'PUT', 'DELETE'])
def func2(id: str):
    if request.method == 'GET':
        result = {
            'Datetime': datetime.now()
        }

    elif request.method == 'PUT':
        result = {
            'Datetime': datetime.now()
        }

    elif request.method == 'DELETE':
        result = {
            'Datetime': datetime.now()
        }

    return jsonify(result)


if __name__ == '__main__':
    client = Connection()

    app.run(host='127.0.0.1', port=5000, debug=True)

    client.close_connection()
