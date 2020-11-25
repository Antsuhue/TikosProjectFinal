from flask import jsonify, request, render_template, url_for, redirect, flash
from datetime import datetime
from flask_weasyprint import render_pdf, HTML
from .pdf_date import verify_pdf_date
from .financial import debit
from ..extensions.db import mongo
from ..model import listProducts as modelListProduct
from ..model import products as modelProduct
from ..model import reportWithdrawProducts as modelWithdraw


format_date = "%d/%m/%Y"
format_time = "%H:%M:%S"


def manageProduct():
    method = request.method

    if method == "POST":
        return new_product()

    elif method == "GET":
        return list_products()


def specify_product(name_product):
    method = request.args["_method"]

    if method == "GET":
        return search_product(name_product)

    elif method == "PUT":
        return edit_product(name_product)

    elif method == "DELETE":
        return remove_product(name_product)


def new_product():
    req = request.form

    dictProduct = {}
    listProducts = []

    product_name = req["nome_produto0"].lower()
    price = req["preco0"].replace(',', '.')

    convert = float(price)
    date = datetime.now()

    list_erro_products = []

    collection_product = mongo.db.products
    collection_report = mongo.db.report

    products = collection_product.find()

    quanti = int(req["quantidade_ingrediente"])
    for each in range(0, quanti):
        pro = "nome_produto" + str(each)
        uni = "unidade" + str(each)
        pre = "preco" + str(each)
        qua = "quantidade" + str(each)
        mini = "min" + str(each)

        formated_nome_produto = req[pro].lower().strip()
        formated_unidade = req[uni].lower()
        formated_preco = req[pre]
        formated_quantidade = req[qua]
        formated_min = req[mini]

        procura_produto = collection_product.find_one({"nome_produto":formated_nome_produto})

        dictProduct = modelProduct.modelProducts(
            formated_nome_produto,
            formated_min,
            formated_quantidade,
            formated_preco,
            formated_unidade)

        if procura_produto == None:
            flash(f"Produto: {product_name} cadastrado!","sucesso")
            collection_product.insert(dictProduct)
        else:
            if formated_nome_produto in list_erro_products:
                pass
            else:
                list_erro_products.append(formated_nome_produto)

    for product in products:
        listProducts.append(product["nome_produto"])

    reportStructure = {
        "nome_produto": req["nome_produto0"].title(),
        "qnt_produtos_inserida": int(req["quantidade0"]),
        "preco_produto": convert,
        "data": date.strftime(format_date),
        "horario": date.strftime(format_time)
    }

    collection_report.insert(reportStructure)

    lenght_list_erro_products = len(list_erro_products)

    if lenght_list_erro_products > 0:
        flash(f"Produtos já existentes: {', '.join(str(x) for x in list_erro_products)}","erro")
        return redirect(url_for("bp.productView"))

    return redirect(url_for("bp.index"))


def list_products():

    listProducts = []

    collection_product = mongo.db.products

    products = collection_product.find()

    for product in products:

        productStructure = modelListProduct.model_list_products(product)

        listProducts.append(productStructure)

    return render_template("Stock.html", listProducts=listProducts)


def search_product():

    req = request.form
    if request.method == "POST":
        name_product = req["produto"].lower()

    listProducts = []
    listProducts2 = []

    collection_product = mongo.db.products

    products2 = collection_product.find()
    products = collection_product.find()

    for product2 in products2:

        productStructure2 = modelListProduct.model_list_products(product2)

        listProducts2.append(productStructure2)

    for product in products:

        if product["nome_produto"] == name_product.lower():
            productStructure = modelListProduct.model_list_products(product)

            listProducts.append(productStructure)

    return render_template("ResultStock.html", listProducts=listProducts, listProducts2=listProducts2)


def sent_new_qntd():
    method = request.method
    req = request.form
    name_product = req["nm_product"]
    new_name = req["new_name"]

    if method == "POST":
        qtd = req["qntd"]
        new_min = req["min"]

        edit_minumum_stock(name_product, new_min)

        return redirect(f"/product/{name_product}/?_method=PUT&qtd={qtd}&new_name={ new_name }")


def edit_product_name(name_product, new_name):

    req = request.json

    collection_product = mongo.db.products

    collection_report = mongo.db.report

    products = collection_product.find()

    alterado = datetime.now()

    search_product = collection_product.find_one({"nome_produto":new_name.lower()})

    for product in products:

        if product["nome_produto"] == name_product.lower():

            if name_product == new_name.lower():
                return(redirect(url_for("bp.index")))

            if search_product != None:
                flash("Nome informado já existente no estoque","erro")
                return(redirect(url_for("bp.index")))

            else:
                flash(f"prato {new_name} atualizado!","sucesso")
                collection_product.update_one(
                                {"nome_produto": name_product.lower()},
                                {"$set": {
                                    "nome_produto": new_name.lower(),
                                    "changed_at": alterado.strftime(format_date)}})

                reportStructure = {
                    "nome_produto": product["nome_produto"],
                    "data": alterado.strftime(format_date),
                    "horario": alterado.strftime(format_time),
                    "status": f"Nome do produto alterado para {new_name.upper()}"
                }

                collection_report.insert(reportStructure)

                return redirect(url_for("bp.index"))

    return jsonify({"status": "Produto nao existe"}), 404


def edit_product(name_product):

    req = request.args
    new_qtd = req["qtd"]
    new_name = req["new_name"].lower()

    collection_product = mongo.db.products

    collection_report = mongo.db.report

    products = collection_product.find()

    alterado = datetime.now()

    for product in products:
        if product["nome_produto"] == name_product.lower():

            collection_product.update_one(
                            {"nome_produto": name_product},
                            {"$set": {
                                "quantidade": int(new_qtd),
                                "changed_at": alterado.strftime(format_date)}})

            reportStructure = {
                "nome_produto": product["nome_produto"],
                "data": alterado.strftime(format_date),
                "horario": alterado.strftime(format_time),
                "status": f"Nome do produto alterado para {new_qtd}"
            }

            collection_report.insert(reportStructure)

            return edit_product_name(name_product, new_name)

    return jsonify({"status": "Produto nao existe 1"}), 404


def edit_minumum_stock(name_product, new_min):

    collection_product = mongo.db.products

    products = collection_product.find()

    for product in products:
        if product["nome_produto"].lower() == name_product.lower():

            collection_product.update_one(
                {
                    "minimo": product["minimo"]
                },
                {
                    "$set": {
                        "minimo" : int(new_min)
                    }
                }
            )


def remove_product(name_product):

    list_products = []

    collection_product = mongo.db.products
    products = collection_product.find()

    collection_report = mongo.db.report

    data = datetime.now()

    for product in products:
        list_products.append(product["nome_produto"])

    if name_product.lower() in list_products:

        reportStructure = {
            "nome_produto": name_product,
            "data": data.strftime(format_date),
            "horario": data.strftime(format_time),
            "status": f"{name_product.upper()} foi removido"
        }

        collection_report.insert_one(reportStructure)
        collection_product.delete_one({'nome_produto': name_product.lower()})

        return redirect(url_for("bp.product"))

    else:
        return jsonify({"Status": "Produto nao encontrado"}), 404


def cashier():
    list_products = list()

    collection_product = mongo.db.products

    products = collection_product.find()

    for product in products:

            list_products.append(product["nome_produto"])

    list_plate = list()

    collection_plate = mongo.db.plates

    plates = collection_plate.find()

    for plate in plates:

        list_plate.append(plate["nome_prato"])

    return render_template("caixa.html", list_products=list_products, list_plate=list_plate)


def add_product():

    method = request.method
    req = request.form

    if method == "POST":
        name_product = req["produto"]
        qntd = req["quantidade"]

    collection_product = mongo.db.products

    products = collection_product.find()

    collection_report = mongo.db.report

    date = datetime.now()

    for product in products:

        if product["nome_produto"].lower() == name_product.lower():

            new_qntd = int(qntd) + int(product["quantidade"])

            gasto = int(qntd) * int(product["preco"])

            reportStructure = {
                "nome_produto": product["nome_produto"],
                "qnt_produtos_adicionados": int(qntd),
                "data": date.strftime(format_date),
                "horario": date.strftime(format_time),
                "gasto": round(gasto, 2)
            }

            debit(gasto)

            collection_report.insert(reportStructure)

            collection_product.update_one(
                                    {"nome_produto": name_product.lower()},
                                    {"$set": {"quantidade": new_qntd}})

            collection_product.update_one(
                        {"nome_produto": name_product.lower()},
                        {"$set": {
                                 "changed_at": date.strftime(format_date)}})

            return redirect(url_for("bp.view_cashier"))

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

            if new_qntd >= 0:

                reportStructure = {
                    "nome_produto": product["nome_produto"],
                    "qnt_produtos_retirados": qntd,
                    "data": date.strftime(format_date),
                    "horario": date.strftime(format_time)
                }

                collection_report.insert(reportStructure)

                collection_product.update_one(
                                    {"nome_produto": name_product.lower()},
                                    {"$set": {"quantidade": new_qntd}})

                collection_product.update_one(
                        {"nome_produto": name_product.lower()},
                        {"$set": {"changed_at": date.strftime(format_date)}})

                return jsonify({"status": "Quantidade retirada"}), 200
            else:
                return jsonify({"status": "Quantidae a ser retirada é maior do que possui no estoque"}), 400

    return jsonify({"status": "Produto nao existe"}), 404


def generate_pdf_products():

    req = request.args

    image_file = url_for('static', filename="images/logo_ticos.png")

    lista = []
    listaReports = []

    collection_product = mongo.db.products
    products = collection_product.find()

    collection_reports = mongo.db.report
    reports = collection_reports.find()

    for product in products:
        dictProduct = {
                    product["nome_produto"]: {"qntd": product["quantidade"],
                                              "preco": str(product["preco"])}}
        lista.append(dictProduct)

    for report in reports:
        if verify_pdf_date(req["inital_date"],report["data"],req["end_date"]) == True:
            if "qnt_produtos_adicionados" in report:
                dictReports = {report["nome_produto"]: {
                            "qntd": report["qnt_produtos_adicionados"],
                            "data": report["data"],
                            "hora": report["horario"],
                            "gasto": str(report["gasto"]),
                            "status": "Adicionou produtos ao estoque"}}
                listaReports.append(dictReports)

            elif "qnt_produtos_retirados" in report:
                dictReports = modelWithdraw.model_report_withdraw_products(report)
                listaReports.append(dictReports)

            elif "qnt_produtos_inserida" in report:
                dictReports = {report["nome_produto"]: {
                            "qntd": report["qnt_produtos_inserida"],
                            "data": report["data"],
                            "hora": report["horario"],
                            "status": "Criação de produto"}}
                listaReports.append(dictReports)

            else:
                dictReports = {report["nome_produto"]: {
                            "data": report["data"],
                            "hora": report["horario"],
                            "status": report["status"]}}
                listaReports.append(dictReports)

    html = render_template("/pdf/pdf_relatorio_produtos.html",
                           lista=lista,
                           listaReport=listaReports,
                           image=image_file)

    return render_pdf(HTML(string=html))
