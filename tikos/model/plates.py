from datetime import datetime

created_at = datetime.now()

format_date = "%d/%m/%Y"
format_time = "%H:%M:%S"


def modelPlate(nome_prato, preco, lista_produtos):

    price = preco.replace(',', '.')
    convert = float(price)
    info_produtos = lista_produtos

    dictPlate = {
        "nome_prato": nome_prato.lower(),
        "preco_prato": round(convert, 2),
        "info_produto": info_produtos,
        "created_at": created_at.strftime(format_date)
    }

    return dictPlate
