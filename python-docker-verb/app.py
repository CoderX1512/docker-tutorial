from flask import Flask, request
from flask_restful import Resource, Api, reqparse

app = Flask(__name__)
api = Api(app)

products = []

parser = reqparse.RequestParser()
parser.add_argument('name', type=str, required=True, help="Product name cannot be blank!")
parser.add_argument('price', type=float, required=True, help="Product price must be provided!")


class ProductResource(Resource):
    def get(self, product_id=None):
        if product_id:
            product = next((prod for prod in products if prod['id'] == product_id), None)
            if product:
                return product, 200
            return {"message": "Product not found"}, 404
        return products, 200

    def post(self):
        args = parser.parse_args()
        product = {
            'id': len(products) + 1,
            'name': args['name'],
            'price': args['price']
        }
        products.append(product)
        return product, 201

    def put(self, product_id):
        args = parser.parse_args()
        product = next((prod for prod in products if prod['id'] == product_id), None)
        if product:
            product['name'] = args['name']
            product['price'] = args['price']
            return product, 200
        return {"message": "Product not found"}, 404

    def delete(self, product_id):
        global products
        products = [prod for prod in products if prod['id'] != product_id ]
        return {"message":"Product deleted"}, 200


api.add_resource(ProductResource, '/product', '/product/<int:product_id>')

if __name__ == "__main__" :
    app.run(host="0.0.0.0", port=5000, debug=True)

