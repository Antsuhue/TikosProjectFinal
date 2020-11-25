def model_list_plate(plate):
    model = {plate["nome_prato"]: {
                    "preco_prato": plate["preco_prato"],
                    "info_produto": plate["info_produto"],
                    "created_at": plate["created_at"]}}

    return model
