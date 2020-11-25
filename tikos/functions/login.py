from flask import request, redirect, url_for, session
from ..extensions.db import mongo

from werkzeug.security import check_password_hash, generate_password_hash

def authLogin():

    req = request.args

    login = req["login"].lower()
    password = req["pass"]

    collection_users = mongo.db.users
    lista = []

    for user in collection_users.find():
        userBd = {
            "login": user["login"].lower(),
            "nome": user["nome_do_usuario"],
            "pass": user["pass"]
        }
        lista.append(userBd)

    for userList in lista:
        if userList["login"] == login and check_password_hash(userList["pass"], password) == True:
            session["login"] = login
            session["nome"] = userList["nome"]
            session.permanent = True

    if "login" in session:
        return redirect(url_for("bp.index"))
    else:
        return redirect(url_for("bp.loginAdm"))


def verify_logged(function):
    if "login" not in session:
        return redirect(url_for("bp.loginAdm"))
    else:
        return function