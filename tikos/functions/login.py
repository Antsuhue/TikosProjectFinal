from flask import request, jsonify, redirect, url_for
from ..extensions.db import mongo

def authLogin():

    req = request.args

    login = req["login"]
    password = req["pass"]

    collection_users = mongo.db.users
    lista = []

    for user in collection_users.find():
        userBd = {
            "login":user["login"],
            "pass":user["pass"]
        }
        lista.append(userBd)
    
    for userList in lista:
        if userList["login"] == login and userList["pass"] == password:
            return redirect(url_for("bp.index"))
        else:
            return redirect(url_for("bp.loginAdm"))