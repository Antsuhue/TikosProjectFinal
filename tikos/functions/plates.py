from flask import jsonify, request, render_template, url_for, redirect, flash
from datetime import datetime
from ..extensions.db import mongo
from .financial import credit
from flask_pymongo import PyMongo, pymongo
from ..model import listPlates as model_list_plate
from ..model import plates as modelPlate


format_date = "%d/%m/%Y"
format_time = "%H:%M:%S"


def managePlate():
    method = request.method

    if method == "POST":
        return new_plate()

    elif method == "GET":
        return list_plates()


def specify_plate(name_plate):
    method = request.args["_method"]

    if method == "GET":
        return search_plate(name_plate)

    elif method == "PUT":
        return edit_plate_qtd(name_plate)

    elif method == "DELETE":
        return remove_plate(name_plate)


def new_plate():
    req = request.form
    dic_plate = {}
    list_plate = []

    plate_name = req["nome_prato"].strip().lower()
    created_at = datetime.now()
    date = datetime.now()

    collection_plate = mongo.db.plates
    collection_reportPlates = mongo.db.reportPlates
    collection_products = mongo.db.products
    plates = collection_plate.find()

    collection_products = mongo.db.products

    lista_produtos = []
    list_not_found_products = []

    for cont in range(0, int(req["quantidade_ingrediente"])):
        p = "product_name" + str(cont)
        q = "product_qntd" + str(cont)
        u = "unidade" + str(cont)

        formated_product_name = req[p].lower().strip()
        formated_product_qntd = req[q].strip()
        formated_unidade = req[u].lower().strip()

        search_product = collection_products.find_one({"nome_produto":formated_product_name})

        if search_product != None:
            lista_produtos.append({"product_name": formated_product_name, "product_qntd": formated_product_qntd, "unidade": formated_unidade})
        else:
            list_not_found_products.append(formated_product_name)

    for plate in plates:
        list_plate.append(plate['nome_prato'])

    dictPlate = modelPlate.modelPlate(req["nome_prato"].lower().strip(), req["preco_prato"].strip(), lista_produtos)

    if plate_name in list_plate:
        flash(f"Prato já existentes: {plate_name}","erro")
        return render_template("formPlates.html")

    elif len(list_not_found_products):
        flash(f"produtos não exitentes: {', '.join(str(item) for item in list_not_found_products)}","erro")
        return redirect(url_for("bp.view_new_plate"))

    else:
        reportStructure = {
        "nome_prato": req["nome_prato"].lower(),
        "preco_prato": req["preco_prato"],
        "data": date.strftime(format_date),
        "horario": date.strftime(format_time)
    }
        collection_reportPlates.insert(reportStructure)
        
        flash(f"{plate_name} cadastrado","Sucesso")
        collection_plate.insert(dictPlate)
        return render_template("formPlates.html")


def list_plates():
    listPlate = []

    collection_plate = mongo.db.plates

    plates = collection_plate.find()

    for plate in plates:

        plateStructure = model_list_plate.model_list_plate(plate)

        listPlate.append(plateStructure)

    return render_template("plates.html", listPlate=listPlate)


def list_ingredients(name_plate):

    listPlate = []

    collection_plate = mongo.db.plates

    plates = collection_plate.find()

    for plate in plates:
        if name_plate.lower() == plate["nome_prato"]:
            length = plate["info_produto"]
            listPlate.append(plate)

    return render_template("updatePlate.html", length=length, listPlate=listPlate)


def search_plate():

    req = request.form
    if request.method == "POST":
        name_plate = req["prato"].lower()

    listPlates1 = []
    listPlates2 = []

    collection_plate = mongo.db.plates

    plates2 = collection_plate.find()
    plates = collection_plate.find()

    for plate2 in plates2:

        plateStructure2 = model_list_plate.model_list_plate(plate2)

        listPlates2.append(plateStructure2)

    for plate in plates:

        if plate["nome_prato"].lower() == name_plate.lower():

            plateStructure = model_list_plate.model_list_plate(plate)

            listPlates1.append(plateStructure)

    return render_template("ResultPlate.html", listPlates1=listPlates1, listPlates2=listPlates2)


def edit_plate():
    listIngredients = []

    method = request.method
    req = request.form
    name_plate = req["current_name"]

    tamanho = int(req["tamanho"])
    for ing in range(tamanho):
        i = "ingrediente" + str(ing)
        q = "quantidade" + str(ing)
        u = "unidade" + str(ing)
        dictIngredients = {"ingredient_name": req[i], "ingredient_quantidade": req[q], "ingredient_unidade": req[u]}
        listIngredients.append(dictIngredients)

    edit_plate_ingredients(name_plate, listIngredients)

    tamanho_add = int(req["tamanhoAdd"])
    listaAdd = []
    for y in range(0, tamanho_add):
        ingrediente_in = "name_ingrediente" + str(y)
        qtd_in = "qtd_ingrediente" + str(y)
        unidade_in = "unidade_ingrediente" + str(y)
        listaAdd.append([req[ingrediente_in], req[qtd_in], req[unidade_in]])

    if method == "POST":
        new_name = req["nome_prato"]
        new_price = req["preco"]

        edit_plate_name(name_plate, new_name)
        edit_plate_qtd(name_plate, new_price, new_name)
        add_products(name_plate, listaAdd)

        return redirect(url_for('bp.plate'))


def edit_plate_ingredients(name_plate, listIngredients):

    collection_plate = mongo.db.plates

    plates = collection_plate.find()

    for plate in plates:

        if name_plate.lower() == plate["nome_prato"]:

            for x in range(0, len(listIngredients)):
                collection_plate.update_many({
                    'info_produto': {
                        '$elemMatch': {
                            'product_name': plate["info_produto"][x]["product_name"],
                            'product_qntd': plate["info_produto"][x]["product_qntd"],
                            'unidade': plate["info_produto"][x]["unidade"]
                            }
                    }
                },
                {"$set": {
                            "info_produto.$.product_name": listIngredients[x]["ingredient_name"],
                            "info_produto.$.product_qntd": listIngredients[x]['ingredient_quantidade'],
                            "info_produto.$.unidade": listIngredients[x]["ingredient_unidade"]
                        }
                    }
                )


def edit_plate_name(name_plate, new_name):

    collection_plate = mongo.db.plates

    collection_reportPlates = mongo.db.reportPlates

    plates = collection_plate.find()

    alterado = datetime.now()

    for plate in plates:

        if plate["nome_prato"] == name_plate.lower():

            collection_plate.update_one(
            {"nome_prato": name_plate.lower()},
            {"$set": {"nome_prato": new_name.lower(),
                "changed_at": alterado.strftime(format_date)}})

            reportStructure = {
                "nome_prato": plate["nome_prato"],
                "data": alterado.strftime(format_date),
                "horario": alterado.strftime(format_time),
                "status": f"Nome do prato alterado para {new_name.upper()}"
            }

            collection_reportPlates.insert(reportStructure)

            return redirect(url_for("bp.plate"))

        return redirect(url_for("bp.plate"))


def edit_plate_qtd(name_plate, new_price, new_name):

    collection_plate = mongo.db.plates
    collection_reportPlates = mongo.db.reportPlates

    plates = collection_plate.find()

    alterado = datetime.now()

    for plate in plates:

        if plate["nome_prato"] == name_plate.lower():

            collection_plate.update_one(
                {"nome_prato": name_plate.lower()},
                {"$set":
                        {"preco_prato": float(new_price),
                        "changed_at": alterado.strftime(format_date)}})

            reportStructure = {
                "nome_prato": plate["nome_prato"],
                "data": alterado.strftime(format_date),
                "horario": alterado.strftime(format_time),
                "status": f"Preço do prato foi alterado para {new_price}"
            }

            collection_reportPlates.insert(reportStructure)


def add_products(name_plate, listaAdd):

    collection_plate = mongo.db.plates

    plates = collection_plate.find()

    for plate in plates:

        if plate["nome_prato"].lower() == name_plate.lower():

            for x in range(0, len(listaAdd)):

                if len(plate["info_produto"]) == 0:
                    collection_plate.update({
                    "nome_prato": plate["nome_prato"]
                    },
                    {"$addToSet": {
                                "info_produto": {"product_name": listaAdd[x][0], "product_qntd": listaAdd[x][1], "unidade": listaAdd[x][2]}
                            }
                    }
                    )
                else:
                    collection_plate.update({
                        'info_produto': {
                            '$elemMatch': {
                                'product_name': plate["info_produto"][x]["product_name"],
                                'product_qntd': plate["info_produto"][x]["product_qntd"],
                                'unidade': plate["info_produto"][x]["unidade"]
                                }
                        }
                    },
                    {"$addToSet": {
                                "info_produto": {"product_name": listaAdd[x][0], "product_qntd": listaAdd[x][1], "unidade": listaAdd[x][2]}
                            }
                        }
                    )


def saida_de_prato():
    req = request.form

    name_plate = req["prato"]
    quantidade = req["quantidade"]

    collection_plate = mongo.db.plates

    plates = collection_plate.find()

    for plate in plates:

        if plate["nome_prato"] == name_plate.lower():

            valor = plate["preco_prato"] * float(quantidade)

            credit(valor)

            return redirect(url_for("bp.view_cashier"))


def remove_plate(name_plate):
    list_plates = []

    collection_plate = mongo.db.plates
    collection_reportPlates = mongo.db.reportPlates

    plates = collection_plate.find()

    data = datetime.now()

    for plate in plates:
        list_plates.append(plate["nome_prato"].lower())

    if name_plate.lower() in list_plates:

        reportStructure = {
                "nome_prato": name_plate,
                "data": data.strftime(format_date),
                "horario": data.strftime(format_time),
                "status": f"{name_plate.upper()} foi removido"
            }

        collection_reportPlates.insert(reportStructure)
        collection_plate.delete_one({'nome_prato': name_plate.lower()})

        return redirect(url_for('bp.plate'))

    else:
        return redirect(url_for('bp.plate'))


def remove_ingredient(name_plate, ingredient_name):

    collection_plate = mongo.db.plates

    plates = collection_plate.find()

    for plate in plates:

        lenPlate = len(plate["info_produto"])
        
        if name_plate.lower() == plate["nome_prato"]:

            for produto in range(0, lenPlate):

                if plate["info_produto"][produto]["product_name"] == ingredient_name.lower():

                    collection_plate.update({'info_produto': {
                        '$elemMatch': {
                            'product_name': plate["info_produto"][produto]["product_name"],
                            'product_qntd': plate["info_produto"][produto]["product_qntd"],
                            'unidade': plate["info_produto"][produto]["unidade"]
                            }}},
                        { "$pull": { "info_produto": { "product_name": ingredient_name.lower()} } })

            return redirect(f'/update/plate/{name_plate}')


def list_form_plate():
    return render_template("formPlates.html")
