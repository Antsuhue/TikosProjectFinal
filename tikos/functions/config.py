from flask import render_template, jsonify, request, url_for, redirect, flash, session
from ..extensions.db import mongo
from ..model.user import model_user
from werkzeug.security import check_password_hash 


def default_configuration():
    collection_config = mongo.db.configuration
    config = collection_config.find()
    list_config = []
    for confguration in config:
        list_config.append(confguration)

    number_employeer = {"empregados":0}
    configuration = [number_employeer]
    collection_config.save()
    return jsonify({"status":"default"})

def list_configuration():
    collection_config = mongo.db.configuration
    collection_users = mongo.db.users
    config = collection_config.find()
    users = collection_users.find()
    list_config = []
    list_users = []

    for confguration in config:
        list_config.append(confguration)

    for user in users:
        list_users.append(user)

    return render_template("config.html", list_users=list_users, list=list_config)

def create_user():
    req = request.args
    name = req["name"]
    login = req["nickname"]
    password = req["pass"]
    re_pass = req["re-pass"]
    listVerify = [name, login, password, re_pass]
    collection_users = mongo.db.users
    list_bd = []


    for user_in_bd in collection_users.find():
        list_bd.append(user_in_bd["login"])

    for item in listVerify:
        if "" == item:
            flash("Um ou mais campos não preenchidos", "erro")
            return redirect(url_for("bp.view_config"))

    for letra in login:
        if " " == letra:
            flash("Não utilize espaços em branco", "erro")
            return redirect(url_for("bp.view_config"))

    if password != re_pass:
        flash("Senhas não coincidem", "erro")
        return redirect(url_for("bp.view_config"))

    if login in list_bd:
        flash("Login já existente", "erro")
        return redirect(url_for("bp.view_config"))

    flash("usuário cadastrado com sucesso", "sucesso")
    collection_users.insert(model_user(name,login,password))
    return redirect(url_for("bp.view_config"))

def delete_user():
    req = request.args
    collection_users = mongo.db.users
    user = collection_users.find_one({"nome_do_usuario":req["nome"]})
    list_users = []

    print(session["nome"])

    if req["nome"] == session["nome"]:
        flash("Não é possível apagar o usuário em sessão","erro")
        redirect(url_for("bp.view_config"))    

    elif check_password_hash(user["pass"], req["password"]) == True:
        flash("Usuário apagado com sucesso!","suceso")
        collection_users.delete_one({"nome_do_usuario":user["nome_do_usuario"]})
        redirect(url_for("bp.view_config"))
    
    else:
        flash("Senha incorreta!","erro")
        redirect(url_for("bp.view_config"))
    
        
    return redirect(url_for("bp.view_config"))
