from flask import Blueprint
from ..functions import products

bp = Blueprint("bp", __name__, static_folder="static", template_folder="template")

def init_app(app):
    app.register_blueprint(bp)

@bp.route("/product", methods=["POST", "DELETE", "GET"])
def index():
    return products.manageProduct()
