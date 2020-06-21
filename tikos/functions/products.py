from flask import jsonify, request, make_response, render_template
from datetime import datetime
import pdfkit
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
    date = datetime.now()

    collection_product = mongo.db.products
    collection_report = mongo.db.report

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

    reportStructure = {
                    "nome_produto": product["nome_produto"],
                    "qnt_produtos_inserida": req["quantidade"],
                    "preco_produto":req["preco"],
                    "data": date.strftime(format_date),
                    "horario":date.strftime(format_time)
                } 

    collection_report.insert(reportStructure)

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

    alterado = datetime.now()

    for product in products:

        if req["nome_produto"] == name_product.lower():
            return jsonify({"status":"Nome digitado é o mesmo que já está cadastrado"}),400

        elif product["nome_produto"] == name_product.lower():
            collection_product.update_one({"nome_produto": name_product.lower()}, {
                                          "$set": {"nome_produto": new_name, "changed_at":alterado.strftime(format_date)}}), 200
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

            reportStructure = {
                "nome_produto": product["nome_produto"],
                "qnt_produtos_adicionados": qntd,
                "data": date.strftime(format_date),
                "horario":date.strftime(format_time),
            }

            collection_report.insert(reportStructure)

            collection_product.update_one({"nome_produto": name_product.lower()}, {
                                          "$set": {"quantidade": new_qntd}})
            collection_product.update_one({"nome_produto": name_product.lower()}, {
                                          "$set": {"changed_at": date.strftime(format_date)}})
            return jsonify({"status": "Quantidade adicionada"}), 200

    return jsonify({"status": "Produto nao existe"}), 404

def withdraw_product(name_product):
    req = request.json

    collection_product = mongo.db.products
    products = collection_product.find()

    collection_report = mongo.db.report

    qntd = req["quantidade"]

    date = datetime.now()
 

    for product in products:
        if product["nome_produto"] == name_product.lower():

            new_qntd = product["quantidade"] - qntd

            if new_qntd >= 0 :

                reportStructure = {
                    "nome_produto": product["nome_produto"],
                    "qnt_produtos_retirados": qntd,
                    "data": date.strftime(format_date),
                    "horario":date.strftime(format_time)
                } 

                collection_report.insert(reportStructure)

                collection_product.update_one({"nome_produto": name_product.lower()}, {
                                            "$set": {"quantidade": new_qntd}})
                collection_product.update_one({"nome_produto": name_product.lower()}, {
                                            "$set": {"changed_at": date.strftime(format_date)}})
                return jsonify({"status": "Quantidade retirada"}), 200
            else:
                return jsonify({"status": "Quantidae a ser retirada é maior do que possui no estoque"}), 400

    return jsonify({"status": "Produto nao existe"}), 404


def generate_pdf_products():

    lista = []
    listaReports = []

    collection_product = mongo.db.products
    products = collection_product.find()

    collection_reports = mongo.db.report
    reports = collection_reports.find()

    for product in products:
        dictProduct = {product["nome_produto"]: {"preco": product["preco"], "quantidade": product["quantidade"], "preco":str(product["preco"])}}
        lista.append(dictProduct)
    
    for report in reports:
        if "qnt_produtos_adicionados" in report:
            dictReports = {report["nome_produto"]: {"qntd": report["qnt_produtos_adicionados"], "data":report["data"], "hora":report["horario"], "gasto": str(report["gasto"]), "status":"Adicionou produtos ao estoque" }}
            listaReports.append(dictReports)

        elif "qnt_produtos_retirados" in report:
            dictReports = {report["nome_produto"]: {"qntd": -report["qnt_produtos_retirados"], "data":report["data"], "hora":report["horario"], "status":"Retirou produtos do estoque" }}
            listaReports.append(dictReports)

        elif "qnt_produtos_inserida" in report:
            dictReports = {report["nome_produto"]: {"qntd": report["qnt_produtos_inserida"], "data":report["data"], "hora":report["horario"], "status":"Criacao de produto"}}
            listaReports.append(dictReports)


    rendered = render_template("pdf_relatorio_produtos.html", lista=lista, listaReport=listaReports)
    # css1 = ['pdf_products.css']
    pdf = pdfkit.from_string(rendered, False)

    response = make_response(pdf)
    response.headers["Content-Type"] = "application/pdf"
    response.headers["Content-Disposition"] = "inline; filename=relatorio0_produtos.pdf"
    
    return response