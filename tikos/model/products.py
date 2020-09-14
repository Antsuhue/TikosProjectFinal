from datetime import datetime

created_at = datetime.now()

format_date = "%d/%m/%Y"
format_time = "%H:%M:%S"

def modelProducts(nome_produto, quantidade, preco):

    price = preco.replace(',','.')
    convert = float(price)

    dictProduct = {
        "nome_produto": nome_produto.lower(),
        "quantidade": int(quantidade),
        "preco":round(convert,2),
    #    "validade": req["validade"],
        "created_at": created_at.strftime(format_date)
    }

    return dictProduct