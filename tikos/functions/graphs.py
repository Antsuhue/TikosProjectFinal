from flask import render_template, request
from ..extensions.db import mongo
from pygal.style import Style
import pygal

def finance_graph():

    collection_debit = mongo.db.debit
    collection_credit = mongo.db.credit

    debit = collection_debit.find()
    credit = collection_credit.find()

    ListaGastos = []
    ListaGanhos = [5, 16]
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
        background='transparent',
        opacity_hover='.9',
        transition='200ms ease-in',
        margin=50
    )
    
    chart = pygal.Bar(
                        title="Financeiro",
                        style=estilos,
                        print_values=True,
                        )

    chart.add("Gastos", ListaGastos)
    chart.add("Ganhos", ListaGanhos)
    chart.add("Lucro/Despesas", ListaLucro)

    chart.x_labels = map(str, sorted(ListaDatas))
    
    grafico = chart.render_data_uri()
    
    return render_template("grafico.html", grafico=grafico)
