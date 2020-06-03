from flask import jsonify, request
from ..extensions.db import mongo


def manageProduct():
    method = request.method

    if method == "POST":
        return add_product()

    elif method == "DELETE":
        return remove_product()

    elif method == "GET":
        return list_products()

def add_product():
    dictProduct = {}
    req = request.json
    listProducts = []

    collection_product = mongo.db.products

    products = collection_product.find()

    for product in products:
        listProducts.append(product["nome_produto"])

    if req["nome_produto"] in listProducts:
        return jsonify({"status": "produto já existente"}), 400

    dictProduct = {
        "nome_produto": req["nome_produto"],
        "quantidade": req["quantidade"],
        "preco": req["preco"],

    }

    collection_product.insert(dictProduct)

    return jsonify({"status": "Adicionado"}), 200


def remove_product():

    req = request.json

    collection_product = mongo.db.products

    products = collection_product.find()
    
    for product in  products:
        if product["nome_produto"] == req["nome_produto"]:
            collection_product.delete_one({'_id':product["_id"]})
            return jsonify({"status":"Produto apagado"}),200
        else:
            return jsonify({"status":"Produto nao existente"}),400

def list_products():
    
    listProducts = []

    collection_product = mongo.db.products
    
    products = collection_product.find()

    for product in products:
        listProducts.append({product["nome_produto"]:{"preco":product["preco"],"quantidade":product["quantidade"]}})

    return jsonify({"produtos":listProducts}),200

    