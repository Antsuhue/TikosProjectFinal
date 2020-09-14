from flask import render_template, request
from ..extensions.db import mongo
from pygal.style import Style
import pygal

def finance_graph():

    collection_debit = mongo.db.debit
    collection_credit = mongo.db.credit

    debit = collection_debit.find()
    credit = collection_credit.find()

    # listaDate = []
    # listaDebit = [] # Gasto
    # listaCredit = [10] # Ganho

    lista = []

    debi = [10, 10, 10]
    cred = [4.6]
    luc = sum(debi)-sum(cred)
    tudo = {}
    print(tudo)

    for deb in debit:
        if deb["createdAt"] not in tudo:
            tudo = {deb["createdAt"]: {"ganho":sum(debi), "gastos":sum(cred), "lucro":luc}}
            cred.append(tudo[from flask import render_template, request
from ..extensions.db import mongo
from pygal.style import Style
import pygal

def finance_graph():

    collection_debit = mongo.db.debit
    collection_credit = mongo.db.credit

    debit = collection_debit.find()
    credit = collection_credit.find()

    # listaDate = []
    # listaDebit = [] # Gasto
    # listaCredit = [10] # Ganho

    lista = []

    debi = [10, 10, 10]
    cred = [4.6]
    luc = sum(debi)-sum(cred)
    tudo = {}
    valores = [0, 0]
    print(tudo)

    for deb in debit:
        if deb["createdAt"] not in tudo:
            tudo = {deb["createdAt"]: {"ganho":sum(debi), "gastos":sum(cred), "lucro":luc}}
            cred.append(tudo[deb["createdAt"]]["gastos"])
        else:
            novo = 10
            tudo[deb["createdAt"]]["ganho"] = tudo[deb["createdAt"]]["ganho"] + novo
            tudo[deb["createdAt"]]["gastos"] = tudo[deb["createdAt"]]["gastos"] + novo
            cred[0] = tudo[deb["createdAt"]]["gastos"]

    print(tudo)
    print(cred)

    # Antsu
    # for deb in debit:
    #     if deb["createdAt"] not in listaDate:
    #         listaDate.append(deb["createdAt"])
    #     lista.append(deb)

    # def findDict(lista, key, valor):
    #     for z, dic in enumerate(lista):
    #         if dic[key] == valor:
    #             return z
    #         return -1

    # for x in lista:
    #     valor = x["valor"]
    #     for t in lista:
    #         if x["createdAt"] == t["createdAt"]:
    #             valor = valor + t["valor"]
    #             index = findDict(lista,"createdAt",t["createdAt"])
    #             lista.pop(index)

    #     listaDebit.append(valor)

    # print("Datas", listaDate)
    # print("Ganho", listaCredit)
    # print("Perda", listaDebit)
    # print(lista)

    # for cred in credit:
    #     listaCredit.append(cred["valor"])

    estilos = Style(
        background='transparent',
        opacity_hover='.9',
        transition='200ms ease-in'
        )

    chart = pygal.Line(
                        title="Financeiro",
                        style= estilos,
                        print_values=True,
                        )

    chart.add('Gastos', cred)#pegar automaticamente os gastos
    chart.add('Faturamento', [19])
    # chart.add('Lucro', tudo['10/09/2020']['lucro'])

    datas = ['10/09/2020', '11/09/2020']
    chart.x_labels = map(str, sorted(datas))

    grafico = chart.render_data_uri()
    return render_template("grafico.html", grafico=grafico)deb["createdAt"]]["gastos"])
        else:
            novo = 10
            tudo[deb["createdAt"]]["ganho"] = tudo[deb["createdAt"]]["ganho"] + novo
            tudo[deb["createdAt"]]["gastos"] = tudo[deb["createdAt"]]["gastos"] + novo
            cred[0] = tudo[deb["createdAt"]]["gastos"]

    print(tudo)
    print(cred)

    # Antsu
    # for deb in debit:
    #     if deb["createdAt"] not in listaDate:
    #         listaDate.append(deb["createdAt"])
    #     lista.append(deb)

    # def findDict(lista, key, valor):
    #     for z, dic in enumerate(lista):
    #         if dic[key] == valor:
    #             return z
    #         return -1

    # for x in lista:
    #     valor = x["valor"]
    #     for t in lista:
    #         if x["createdAt"] == t["createdAt"]:
    #             valor = valor + t["valor"]
    #             index = findDict(lista,"createdAt",t["createdAt"])
    #             lista.pop(index)

    #     listaDebit.append(valor)

    # print("Datas", listaDate)
    # print("Ganho", listaCredit)
    # print("Perda", listaDebit)
    # print(lista)

    # for cred in credit:
    #     listaCredit.append(cred["valor"])

    estilos = Style(
        background='transparent',
        opacity_hover='.9',
        transition='200ms ease-in'
        )

    chart = pygal.Line(
                        title="Financeiro",
                        style= estilos,
                        print_values=True,
                        )

    chart.add('Gastos', cred)#pegar automaticamente os gastos
    chart.add('Faturamento', [19])
    # chart.add('Lucro', tudo['10/09/2020']['lucro'])

    datas = ['10/09/2020', '11/09/2020']
    chart.x_labels = map(str, sorted(datas))

    grafico = chart.render_data_uri()
    return render_template("grafico.html", grafico=grafico)
