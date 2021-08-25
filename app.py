import json

from flask import Flask, jsonify, request, make_response
from flask_restx import Api, Resource, fields, reqparse
from werkzeug.middleware.proxy_fix import ProxyFix
from os import environ
from app.card_hash import card_hash


app = Flask(__name__)
app.wsgi_app = ProxyFix(app.wsgi_app)
api = Api(app, version='1.0', title='Pagarme card_hash com Python - API',
    description='Api to Card_hash generation and data encryption for Pagarme in Python.'
                ' https://docs.pagar.me/reference#gerando-card_hash-manualmente',)


ns = api.namespace('api/v1/card_hash', description='Geração de card_hash encritação de dados para o Pagarme em Python')

model = api.model('Card', {
    'card_number': fields.String(required=True, description='Card Number' ),
    'card_holder_name': fields.String(required=True, description='Holder Name'),
    'card_expiration_date': fields.String(required=True, description='Expiration Date'),
    'card_cvv': fields.String(required=True, description='CVV')
})

parser = reqparse.RequestParser()
parser.add_argument("card_number", location="json", type=str)
parser.add_argument("card_holder_name", location="json", type=str)
parser.add_argument("card_expiration_date", location="json", type=str)
parser.add_argument("card_cvv", location="json", type=str)


class CardHash(object):
    def __init__(self):
        self.counter = 0

    def create(self, data):
        return make_response(jsonify({"card_hash": card_hash(data)}), 200)
        api.abort(404, "Card {} doesn't exist".format(card_hash(data)))


DAO = CardHash()

@ns.route('/')
@ns.response(200, 'Ok')
@ns.response(404, 'Bank not found')
class Hash(Resource):
    @ns.expect(model)
    def post(self):
        return DAO.create(request.json)


if __name__ == '__main__':
    SERVER_HOST = environ.get('SERVER_HOST', 'localhost')
    app.run(host=SERVER_HOST, port=5500, debug=(not environ.get('ENV') == 'PRODUCTION'), threaded=True)
    app.run(debug=True)