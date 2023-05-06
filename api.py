from flask import Flask
from flask_restful import Api, Resource, reqparse

app = Flask(__name__)
api = Api(app)

helloworld_parser = reqparse.RequestParser()
helloworld_parser.add_argument(
    'name', type=str, help='Name of the person', location='form', required=True)
helloworld_parser.add_argument(
    'email', type=str, help='Email of the person', location='form', required=True)
helloworld_parser.add_argument(
    'password', type=str, help='Password of the person', location='form', required=True)


class HelloWorld(Resource):
    def get(self, name):
        return {'data': f'Hello {name}!'}

    def post(self):
        args = helloworld_parser.parse_args()
        name = args.get('name')
        email = args.get('email')
        password = args.get('password')
        print(name, email, password)
        return {'data': 'Posted'}


class Second(Resource):
    def post(self):
        return {'data': 'Second'}


api.add_resource(HelloWorld, '/hello')
api.add_resource(Second, '/second')

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)
