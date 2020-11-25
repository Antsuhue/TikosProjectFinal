from flask import Blueprint, render_template, request, redirect, session, url_for
from ..functions import products, financial, plates, login, config, logout, manage_pdf


bp = Blueprint(
                "bp", __name__,
                static_folder="static",
                template_folder="templates")


def init_app(app):
    app.register_blueprint(bp)


@bp.route("/", methods=["GET"])
def index():
    return login.verify_logged(products.list_products())


@bp.route("/login")
def loginAdm():
    if "login" not in session:
        return render_template("index.html")
    else:
        return redirect(url_for("bp.index"))


@bp.route('/auth', methods=["GET"])
def auth():
    return login.verify_logged(login.authLogin())


@bp.route("/product/new/", methods=["GET"])
def productView():
    return login.verify_logged(render_template("formProducts.html"))


@bp.route("/product/", methods=["POST", "GET"])
def product():
    return login.verify_logged(products.manageProduct())


@bp.route("/product/<name_product>/", methods=["GET", "PUT", "DELETE"])
def find_product(name_product):
    return login.verify_logged(products.specify_product(name_product.lower()))


@bp.route("/product/add_qntd/", methods=["POST"])
def add_qnt_produtcs():
    return login.verify_logged(products.add_product())


@bp.route("/product/withdraw_qntd/<name_product>/", methods=["PUT"])
def withdraw_qnt_produtcs(name_product):
    return login.verify_logged(products.withdraw_product(name_product.lower()))


@bp.route("/product/edit_qntd", methods=["POST"])
def edit_qnt_produtcs():
    return login.verify_logged(products.sent_new_qntd())


@bp.route("/pdf/")
def pdf():
    req = request.args
    return login.verify_logged(manage_pdf.select_pdf(req["tipo_pdf"]))

@bp.route("/financial/", methods=["GET"])
def view_financial():
    return login.verify_logged(financial.finance_graph())


@bp.route("/financial/new/", methods=["POST"])
def new_financial():
    return login.verify_logged(financial.new())


@bp.route("/plate/", methods=["POST", 'GET'])
def plate():
    return login.verify_logged(plates.managePlate())


@bp.route("/new_plate/")
def view_new_plate():
    return login.verify_logged(plates.list_form_plate())


@bp.route("/search_product", methods=["POST"])
def search_product():
    return login.verify_logged(products.search_product())


@bp.route("/plate/<name_plate>/", methods=["GET", "PUT", "DELETE"])
def find_plate(name_plate):
    return login.verify_logged(plates.specify_plate(name_plate.lower()))


@bp.route("/plate/edit_qntd", methods=["POST"])
def edit_qnt_plate():
    return login.verify_logged(plates.edit_plate())


@bp.route("/update/plate/<name_plate>", methods=["get"])
def updatePlate(name_plate):
    return login.verify_logged(plates.list_ingredients(name_plate))


@bp.route("/search_plate", methods=["POST"])
def search_plate():
    return login.verify_logged(plates.search_plate())


@bp.route("/delete_ingredient/<name_plate>/<ingredient_name>")
def delete_ingredient(name_plate, ingredient_name):
    return login.verify_logged(plates.remove_ingredient(name_plate, ingredient_name))


@bp.route("/reports/", methods=["GET"])
def view_reports():
    return login.verify_logged(financial.reports())


@bp.route("/logout/")
def logout_session():
    logout.logout_app()
    return login.verify_logged(redirect(url_for("bp.loginAdm")))


@bp.route("/config/", methods=["GET"])
def view_config():
     return login.verify_logged(config.list_configuration())


@bp.route("/default_config/", methods=["GET"])
def default_config():
    return login.verify_logged(config.default_configuration())


@bp.route("/new_user/", methods=["GET"])
def new_user():
    return login.verify_logged(config.create_user())


@bp.route("/delete_user/")
def delete_users():
    return login.verify_logged(config.delete_user())


@bp.route("/caixa/")
def view_cashier():
    return login.verify_logged(products.cashier())


@bp.route("/baixa/", methods=["POST"])
def abatimento():
    return login.verify_logged(plates.saida_de_prato())
