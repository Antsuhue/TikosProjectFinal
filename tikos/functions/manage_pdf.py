from flask import request
from .products import generate_pdf_products
from datetime import datetime


format_date = "%d/%m/%Y"
format_time = "%H:%M:%S"

def select_pdf(type):
    if type == "estoque":
        return generate_pdf_products()
    else:
        return "<H1> PDF em Desenvolvimento </H1>"
