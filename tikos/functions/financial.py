from flask import jsonify, request, render_template
from ..extensions.db import mongo
from datetime import datetime
from pygal.style import Style
import pygal

format_date = "%d/%m/%Y"
format_time = "%H:%M:%S"
createdAt = datetime.now()


def credit(value):
    collection_credit = mongo.db.credit

    fin = {
        "valor":round(value,2),
        "createdAt":createdAt.strftime(format_date)
    }
    collection_credit.insert(fin)

    return jsonify({"Credit":"fim"})

def debit(value):
    collection_debit = mongo.db.debit

    fin = {
        "valor":round(value,2),
        "createdAt":createdAt.strftime(format_date)
    }

    collection_debit.insert(fin)

    return jsonify({"Debit": "fim"})

def finance_graph():

    collection_debit = mongo.db.debit
    collection_credit = mongo.db.credit

    debit = collection_debit.find()
    credit = collection_credit.find()

    ListaGastos = []
    ListaGanhos = [554, 216, 3200, 125, 250, 978, 755, 122, 6897, 1215, 1234, 789]
    ListaLucro = []
    ListaDatas = [] #essa vale
    ListaDatas1 = []

    """ Fazer verificação se ele Perde """

    for deb in debit:#Recebo a data e o valor e faço a verificação
        if deb["createdAt"] not in ListaDatas:#if a data ainda não estiver na ListaDatas:
            ListaDatas.append(deb["createdAt"])#ele adiciona a data na ListaDatas 
            ListaGastos.append(deb["valor"])#pega o valor e adiciona na listaGastos
        else:#else: #se a data já estiver dentro de ListaDatas
            ListaGastos[len(ListaGastos)-1] += deb["valor"] #ListaGastos[len(ListaGastos)-1] += valor recebido

    """ Fazer verificação se ele Ganha """

    for deb1 in credit:#Recebo a data e o valor e faço a verificação 
        if deb1["createdAt"] not in ListaDatas1:#if a data ainda não estiver na ListaDatas1:
            ListaDatas1.append(deb1["createdAt"])#ele adiciona a data na ListaDatas 
            ListaGanhos.append(deb1["valor"])#pega o valor e adiciona na listaGanhos
        else:#else: #se a data já estiver dentro de ListaDatas
            ListaGanhos[len(ListaGanhos)-1] += deb1["valor"]#ListaGanhos[len(ListaGanhos)-1] += valor recebido

    """ Fazer calculo """
    for i in range(len(ListaDatas)):#para cada data na ListaDatas e ele pega o len e vai calculando
        ListaLucro.append(ListaGanhos[i]-ListaGastos[i])

    estilos = Style(
        plot_background="#E5E5E2",
        background="#E5E5E2",
        opacity='.9',
        # opacity_hover='.9',
        transition='200ms ease-in',
        
        colors=('#3F1052', '#a3b637', '#E95355'),

        font_family="Poppins, sans-serif",
        label_font_family="Poppins, sans-serif",

        title_font_size= 100,
        tooltip_font_size=100,

        major_label_font_size=100, #numeros maiores
        label_font_size=70,
        legend_font_size= 80,
    )

    chart = pygal.StackedBar(
                        title="",
                        style=estilos,
                        print_values=False,
                        width=4000,
                        height=2800,
                        rounded_bars=8,
                        tooltip_border_radius=20,
                        legend_box_size=100
                        )

    chart.add("Gastos", ListaGastos)
    chart.add("Faturamento", ListaGanhos)
    chart.add("Lucro/Prejuizo", ListaLucro)

    chart.x_labels = map(str, sorted(ListaDatas))
    
    grafico = chart.render_data_uri()
    
    return render_template("finances.html", grafico=grafico)

def reports():
    return render_template("reports.html")