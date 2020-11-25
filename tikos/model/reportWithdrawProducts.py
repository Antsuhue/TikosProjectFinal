from datetime import datetime

created_at = datetime.now()

format_date = "%d/%m/%Y"
format_time = "%H:%M:%S"


def model_report_withdraw_products(report):

    dictProduct = {
        report["nome_produto"]: {
                    "qntd": -report["qnt_produtos_retirados"],
                    "data": report["data"],
                    "hora": report["horario"],
                    "status": "Retirou produtos do estoque"}
    }

    return dictProduct
