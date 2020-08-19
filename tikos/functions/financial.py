from flask import jsonify, request
from ..extensions.db import mongo
from datetime import datetime

format_date = "%d/%m/%Y"
format_time = "%H:%M:%S"
createdAt = datetime.now()


def credit(value):
    collection_financial = mongo.db.financial

    fin = {
        "valor":value,
        "createdAt":createdAt.strftime(format_date)
    }
    collection_financial.insert(fin)

    return jsonify({"financial":"fim"})

def debit(value):
    collection_financial = mongo.db.financial
    
    fin = {
        "valor":value,
        "createdAt":createdAt.strftime(format_date)
    }
    collection_financial.insert(fin)

    return jsonify({})
