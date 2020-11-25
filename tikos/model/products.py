from datetime import datetime

created_at = datetime.now()

format_date = "%d/%m/%Y"
format_time = "%H:%M:%S"


def modelProducts(nome_produto, min, quantidade, preco, unidade):

    price = preco.replace(',', '.')
    convert = float(price)

    dictProduct = {
        "nome_produto": nome_produto.lower(),
        "minimo": int(min),
        "quantidade": int(quantidade),
        "preco": round(convert, 2),
        "created_at": created_at.strftime(format_date),
        "unidade": unidade.lower()
    }

    return dictProduct
