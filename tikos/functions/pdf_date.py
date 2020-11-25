from datetime import datetime

format_date = "%d/%m/%Y"
format_time = "%H:%M:%S"

def verify_pdf_date(data_inicio, data ,data_fim):
    
    data_inicial = data_inicio.split('-')
    ano_inicio = int(data_inicial[0])
    mes_inicio = int(data_inicial[1])
    dia_inicio = int(data_inicial[2])
    data_inicial_formatada = datetime(ano_inicio, mes_inicio, dia_inicio)


    data_bd = data.split('/')
    ano_bd = int(data_bd[2])
    mes_bd = int(data_bd[1])
    dia_bd = int(data_bd[0])
    data_bd_formatada = datetime(ano_bd, mes_bd, dia_bd)

    data_final = data_fim.split('-')
    ano_final = int(data_final[0])
    mes_final = int(data_final[1])
    dia_final = int(data_final[2])
    data_final_formatada = datetime(ano_final, mes_final, dia_final)

    return data_inicial_formatada <= data_bd_formatada <= data_final_formatada
