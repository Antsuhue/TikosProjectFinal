def model_list_products(product):
    model = {product["nome_produto"]: {
                    "preco": product["preco"],
                    "minimo": product["minimo"],
                    "quantidade": int(product["quantidade"]),
                    "unidade": product["unidade"],
                    "created_at": product["created_at"]}}

    return model