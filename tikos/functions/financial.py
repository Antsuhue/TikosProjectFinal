from flask import jsonify, request
from ..extensions.db import mongo
from datetime import datetime

format_date = "%d/%m/%Y"
format_time = "%H:%M:%S"
createdAt = datetime.now()


def credit(value):
    collection_credit = mongo.db.credit

    fin = {
        "valor":round(value,2),
        "createdAt":createdAt.strftime(format_date)
    }
    collection_credit.insert(fin)

    return jsonify({"Credit":"fim"})

def debit(value):
    collection_debit = mongo.db.debit

    fin = {
        "valor":round(value,2),
        "createdAt":createdAt.strftime(format_date)
    }

    collection_debit.insert(fin)

    return jsonify({"Debit": "fim"})
