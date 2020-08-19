from flask import jsonify, request, make_response, render_template,url_for
from datetime import datetime
from flask_weasyprint import HTML, render_pdf
import base64
from ..extensions.db import mongo


format_date = "%d/%m/%Y"
format_time = "%H:%M:%S"


def managePlate():
    method = request.method

    if method == "POST":
        return new_plate()

    elif method == "GET":
        return list_plates()


def specify_plate(name_plate):
    method = request.method

    if method == "GET":
        return search_plate(name_plate)

    elif method == "PUT":
        return edit_plate_name(name_plate)

    elif method == "DELETE":
        return remove_plate(name_plate)


def new_plate():
    req = request.json
    dic_plate = {}
    list_plate = []

    plate_name = req['nome_prato'].lower()
    created_at = datetime.now()
    date = datetime.now()

    collection_plate = mongo.db.plates
    collection_reportPlates = mongo.db.report

    plates = collection_plate.find()

    for plate in plates:
        list_plate.append(plate['nome_prato'])

    if plate_name in list_plate:
        return jsonify({"status": "plate já existente"}), 404

    dic_plate = {
        'nome_prato': req['nome_prato'].lower(),
        'ingredientes': req['ingredientes'],
        'preco_prato': req['preco_prato'],
        'created_at': created_at.strftime(format_date)
    }

    reportStructure = {
        "nome_prato": req["nome_prato"].lower(),
        "preco_prato": req["preco_prato"],
        "data": date.strftime(format_date),
        "horario":date.strftime(format_time)
    }

    collection_plate.insert(dic_plate)
    collection_reportPlates.insert(reportStructure)

    return jsonify({'status': 'Adicionado'}), 200


def list_plates():

    listPlate = []

    collection_plate = mongo.db.plates

    plates = collection_plate.find()

    for plate in plates:

        plateStructure = {plate["nome_prato"]: {"preco_prato": plate["preco_prato"],
                                                "ingredientes": plate["ingredientes"],
                                                "created_at": plate["created_at"]}}

        listPlate.append(plateStructure)

    return jsonify({"pratos": listPlate}), 200


def search_plate(name_plate):

    collection_plate = mongo.db.plates

    plates = collection_plate.find()

    for plate in plates:
        if plate['nome_prato'] == name_plate.lower():
            return jsonify({plate['nome_prato']: {'preco_prato': plate['preco_prato'], 'ingredientes': plate['ingredientes']}})

    return jsonify({"status": "Prato nao existe"}), 404


def edit_plate_name(name_plate):
    req = request.json
    new_name = req['nome_prato'].lower()

    collection_plate = mongo.db.plates
    collection_reportPlates = mongo.db.report

    plates = collection_plate.find()

    alterado = datetime.now()

    for plate in plates:

        if req["nome_prato"] == name_plate.lower():

            return jsonify({"status":"Nome digitado é o mesmo que já está cadastrado"}), 400

        elif plates["nome_prato"] == name_plate.lower():

            collection_plate.update_one({"nome_prato": name_plate.lower()},
                                        {"$set": {"nome_prato": new_name, "changed_at":alterado.strftime(format_date)}})

            reportStructure = {
                "nome_prato": plate["nome_prato"],
                "data": alterado.strftime(format_date),
                "horario": alterado.strftime(format_time),
                "status": f"Nome do prato alterado para {new_name.upper()}"
            }

            collection_reportPlates.insert(reportStructure)

            return jsonify({"status": "Nome alterado"}), 200

    return jsonify({"status": "Prato nao existe"}), 404


def remove_plate(name_plate):
    list_plates = []

    collection_plate = mongo.db.plates
    collection_reportPlates = mongo.db.report

    plates = collection_plate.find()

    data = datetime.now()

    for plate in plates:
        list_plates.append(plate["nome_prato"].lower())

    if name_plate.lower() in list_plates:

        reportStructure = {
                "nome_prato": name_plate,
                "data": data.strftime(format_date),
                "horario":data.strftime(format_time),
                "status": f"{name_plate.upper()} foi removido"
            }

        collection_reportPlates.insert(reportStructure)
        collection_plate.delete_one({'nome_prato': name_plate.lower()})

        return jsonify({"Status": "Prato apagado"}), 200

    else:
        return jsonify({"Status": "Prato nao encontrado"}), 404

