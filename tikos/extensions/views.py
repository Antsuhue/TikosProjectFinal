import os
from flask import Blueprint,render_template, send_from_directory, redirect, url_for
from ..functions import products, financial, plates, login, graphs

bp = Blueprint("bp", __name__, static_folder="static", template_folder="templates")

def init_app(app):
    app.register_blueprint(bp)

@bp.route("/", methods=["GET"])
def index():
    return products.list_products()

@bp.route("/login")
def loginAdm():
    return render_template("index.html")

@bp.route('/auth', methods=["GET"])
def auth():
    return login.authLogin()

@bp.route("/product/new/")
def productView():
    return render_template("formProducts.html")

@bp.route("/product/", methods=["POST", "GET"])
def product():
    return products.manageProduct()

@bp.route("/product/<name_product>/", methods=["GET", "PUT", "DELETE"])
def find_product(name_product):
    return products.specify_product(name_product.lower())

@bp.route("/product/add_qntd/<name_product>/", methods=["PUT"])
def add_qnt_produtcs(name_product):
    return products.add_product(name_product.lower())

@bp.route("/product/withdraw_qntd/<name_product>/", methods=["PUT"])
def withdraw_qnt_produtcs(name_product):
    return products.withdraw_product(name_product.lower())

@bp.route("/pdf/")
def pdf():
    return products.generate_pdf_products()

@bp.route("/financial/", methods=["GET"])
def view_financial():
    # return render_template("finances.html")
    return financial.finance_graph()

@bp.route("/financial/new/", methods=["POST"])
def new_financial():
    return financial.new()

@bp.route("/plate/", methods=["POST", 'GET'])
def plate():
    return plates.managePlate()

@bp.route("/plates/")
def view_plates():
    return render_template("formPlates.html")

@bp.route("/plate/<name_plate>/", methods=["GET", "PUT", "DELETE"])
def find_plate(name_plate):
    return plates.specify_plate(name_plate.lower())

@bp.route("/reports/", methods=["GET"])
def view_reports():
    return financial.reports()