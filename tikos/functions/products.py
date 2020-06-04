from flask import jsonify, request
from datetime import datetime
from ..extensions.db import mongo


format_date = "%d/%m/%Y"
format_time = "%H:%M:%S"


def manageProduct():
    method = request.method

    if method == "POST":
        return new_product()

    elif method == "GET":
        return list_products()


def specify_product(name_product):
    method = request.method

    if method == "GET":
        return search_product(name_product)

    elif method == "PUT":
        return edit_product_name(name_product)

    elif method == "DELETE":
        return remove_product(name_product)


def new_product():
    dictProduct = {}
    req = request.json
    listProducts = []
    product_name = req["nome_produto"].lower()
    created_at = datetime.now()

    collection_product = mongo.db.products

    products = collection_product.find()

    for product in products:
        listProducts.append(product["nome_produto"])

    if product_name in listProducts:
        return jsonify({"status": "produto já existente"}), 404

    dictProduct = {
        "nome_produto": req["nome_produto"].lower(),
        "quantidade": req["quantidade"],
        "preco": req["preco"],
        "created_at": created_at.strftime(format_date)

    }

    collection_product.insert(dictProduct)

    return jsonify({"status": "Adicionado"}), 200


def list_products():

    listProducts = []

    collection_product = mongo.db.products

    products = collection_product.find()

    for product in products:

        productStructure = {product["nome_produto"]: {"preco": product["preco"],
                                                      "quantidade": product["quantidade"],
                                                      "created_at": product["created_at"]}}

        listProducts.append(productStructure)

    return jsonify({"produtos": listProducts}), 200


def search_product(name_product):

    collection_product = mongo.db.products

    products = collection_product.find()

    for product in products:
        if product["nome_produto"] == name_product.lower():
            return jsonify({product["nome_produto"]: {"preco": product["preco"], "quantidade": product["quantidade"]}})

    return jsonify({"status": "Produto nao existe"}), 404


def edit_product_name(name_product):

    req = request.json
    new_name = req["nome_produto"].lower()

    collection_product = mongo.db.products

    products = collection_product.find()

    for product in products:
        if product["nome_produto"] == name_product.lower():
            collection_product.update_one({"nome_produto": name_product.lower()}, {
                                          "$set": {"nome_produto": new_name}}), 200
            return jsonify({"status": "Nome alterado"}), 200

    return jsonify({"status": "Produto nao existe"}), 404


def remove_product(name_product):

    collection_product = mongo.db.products
    products = collection_product.find()

    list_products = []

    for product in products:
        list_products.append(product["nome_produto"])

    if name_product.lower() in list_products:
        collection_product.delete_one({'nome_produto': name_product.lower()})
        return jsonify({"Status": "Produto apagado"}), 200

    else:
        return jsonify({"Status": "Produto nao encontrado"}), 404


def add_product(name_product):

    req = request.json

    collection_product = mongo.db.products
    products = collection_product.find()

    collection_report = mongo.db.report

    qntd = req["quantidade"]

    date = datetime.now()


    for product in products:
        if product["nome_produto"] == name_product.lower():

            new_qntd = qntd + product["quantidade"]

            spend = qntd * product["preco"]

            reportStructure = {
                "nome_produto": product["nome_produto"],
                "qnt_produtos_adicionados": qntd,
                "data": date.strftime(format_date),
                "horario":date.strftime(format_time),
                "gasto": spend
            }

            collection_report.insert(reportStructure)

            collection_product.update_one({"nome_produto": name_product.lower()}, {
                                          "$set": {"quantidade": new_qntd}})
            collection_product.update_one({"nome_produto": name_product.lower()}, {
                                          "$set": {"changed_at": date.strftime(format_date)}})
            return jsonify({"status": "Quantidade adicionada"}), 200

    return jsonify({"status": "Produto nao existe"}), 404

def withdraw_product(name_product):
    pass
