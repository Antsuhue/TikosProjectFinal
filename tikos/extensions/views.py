import os
from flask import Blueprint,render_template, send_from_directory
from ..functions import products

bp = Blueprint("bp", __name__, static_folder="static", template_folder="template")

def init_app(app):
    app.register_blueprint(bp)

@bp.route('/favicon.ico')
def favicon():  
    return send_from_directory(os.path.join(bp.root_path, 'static'), 'favicon.ico', mimetype='static/favicon.ico')

@bp.route("/", methods=["POST", "GET"])
def index():
    return render_template("index.html")

@bp.route("/product", methods=["POST", "GET"])
def product():
    return products.manageProduct()

@bp.route("/product/<name_product>", methods=["GET", "PUT", "DELETE"])
def find_product(name_product):
    return products.specify_product(name_product.lower())

@bp.route("/product/add_qntd/<name_product>", methods=["PUT"])
def add_qnt_produtcs(name_product):
    return products.add_product(name_product.lower())

@bp.route("/product/withdraw_qntd/<name_product>", methods=["PUT"])
def withdraw_qnt_produtcs(name_product):
    return products.withdraw_product(name_product.lower())

@bp.route("/pdf")
def pdf():
    return products.generate_pdf_products()
