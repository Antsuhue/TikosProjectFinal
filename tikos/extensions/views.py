from flask import Blueprint
from ..functions import products

bp = Blueprint("bp", __name__, static_folder="static", template_folder="template")

def init_app(app):
    app.register_blueprint(bp)

@bp.route("/product", methods=["POST", "GET"])
def product():
    return products.manageProduct()

@bp.route("/product/<name_product>", methods=["GET", "PUT", "DELETE"])
def find_product(name_product):
    return products.specify_product(name_product.lower())

@bp.route("/product/add_qntd/<name_product>", methods=["PUT"])
def add_qnt_produtcs(name_product):
    return products.add_product(name_product.lower())
