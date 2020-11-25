from flask import jsonify, render_template
from ..extensions.db import mongo
from datetime import datetime
from pygal.style import Style
import pygal

format_date = "%d/%m/%y"
format_time = "%H:%M:%S"
createdAt = datetime.now()


def credit(value):
    collection_credit = mongo.db.credit

    fin = {
        "valor": round(value, 2),
        "createdAt": createdAt.strftime(format_date)
    }
    collection_credit.insert(fin)

    return jsonify({"Credit": "fim"})


def debit(value):
    collection_debit = mongo.db.debit

    fin = {
        "valor": round(value, 2),
        "createdAt": createdAt.strftime(format_date)
    }

    collection_debit.insert(fin)

    return jsonify({"Debit": "fim"})


def finance_graph():

    collection_debit = mongo.db.debit
    collection_credit = mongo.db.credit

    debit = collection_debit.find()
    credit = collection_credit.find()

    ListaGastos = []
    ListaGanhos = []
    ListaLucro = []

    ListaDatas = []  # essa vale
    ListaDatas1 = []

    for deb in debit:
        if deb["createdAt"] not in ListaDatas:
            ListaDatas.append(deb["createdAt"])
            ListaGastos.append(deb["valor"])
        else:
            ListaGastos[len(ListaGastos)-1] += deb["valor"]

    for cred in credit:
        if cred["createdAt"] not in ListaDatas1:
            ListaDatas1.append(cred["createdAt"])
            ListaGanhos.append(cred["valor"])
        else:
            ListaGanhos[len(ListaGanhos)-1] += cred["valor"]

    for i in range(len(ListaDatas)):
        ListaLucro.append(ListaGanhos[i]-ListaGastos[i])

    return render_template(
                            "finances.html",
                            grafico=firstGraphic(ListaGastos, ListaGanhos, ListaLucro, ListaDatas),
                            grafico2=secondGraphic(ListaDatas, ListaGanhos),
                            grafico3=thirdGraphic())


def firstGraphic(ListaGastos, ListaGanhos, ListaLucro, ListaDatas):

    estilos = Style(
    plot_background="#E5E5E2", # Cor de trás do grafico
    background="#E5E5E2", # Cor de trás da imagem do grafico
    foreground_subtle="#000000",
    opacity='.9', # opacidade
    transition='200ms ease-in',

    colors=('#3F1052', '#a3b637', '#E95355'),

    font_family="Poppins, sans-serif",
    label_font_family="Poppins, sans-serif",
    title_font_size=40,

    tooltip_font_size=50, # tamanho do resultado de cada bolinha

    major_label_font_size=20, # tamanho da fonte do rótulo principal
    label_font_size=15, # tamanho da fonte da etiqueta
    legend_font_size=23, # tamanho das legendas
    )

    chart = pygal.Line(
                        title="Informações Gerais",
                        style=estilos,
                        legend_box_size=30,
                        legend_at_bottom=True,
                        legend_at_bottom_columns=3,
                        tooltip_border_radius=20,
                        )

    chart.add("Gastos", ListaGastos)
    chart.add("Faturamento", ListaGanhos)
    chart.add("Lucro/Prejuizo", ListaLucro)

    chart.x_labels = map(str, ListaDatas)

    grafico = chart.render_data_uri()

    return grafico


def secondGraphic(ListaDatas, ListaGastos):
    # Semana
    ListaSemana = []
    SemanaGastos = []
    for semana in ListaDatas:
        if len(ListaSemana) == 7:
            ListaSemana = []
            SemanaGastos = []
            ListaSemana.append(semana)
            SemanaGastos.append(ListaGastos[-1])
        else:
            ListaSemana.append(semana)
            SemanaGastos.append(ListaGastos[-1])

    # Ano
    ListaAno = []
    AnoGastos = []
    for ano in ListaDatas:
        if len(ListaAno) == 366:
            ListaAno = []
            AnoGastos = []
            ListaAno.append(ano)
            AnoGastos.append(ListaAno[-1])
        else:
            ListaAno.append(ano)
            AnoGastos.append(ListaGastos[-1])

    estilos2 = Style(
        plot_background="#E5E5E2",
        background="#E5E5E2",
        opacity='.9',
        foreground_subtle="#000000",
        opacity_hover='.9',
        transition='200ms ease-in',

        colors=('#8b35ad', '#69c812', '#0874d6'),

        font_family="Poppins, sans-serif",
        value_font_family="Poppins, sans-serif",
        label_font_family="Poppins, sans-serif",

        legend_font_size=23,
        title_font_size=55,

        tooltip_font_size=40,
        value_font_size=100,
    )

    chart2 = pygal.Pie(
                        title="Gastos",
                        style=estilos2,
                        legend_box_size=50,
                        legend_at_bottom=True,
                        legend_at_bottom_columns=3,
                        tooltip_border_radius=20,
                        )

    chart2.add("Semanal", sum(SemanaGastos))
    chart2.add("Mensal", 500)
    chart2.add("Anual", sum(AnoGastos))

    grafico2 = chart2.render_data_uri()

    return grafico2


def thirdGraphic():
    estilos3 = Style(
        plot_background="#E5E5E2",
        background="#E5E5E2",
        opacity='.9',
        foreground_subtle="#000000",
        transition='200ms ease-in',

        colors=('#E95355', '#088A85', '#58FA82'),

        font_family="Poppins, sans-serif",
        value_font_family="Poppins, sans-serif",
        label_font_family="Poppins, sans-serif",

        legend_font_size=23,
        title_font_size=55,
        tooltip_font_size=50,

        value_font_size=100,
    )

    chart3 = pygal.Pie(
                        title="Gastos p/ Categoria",
                        style=estilos3,
                        legend_box_size=50,
                        legend_at_bottom=True,
                        legend_at_bottom_columns=3,
                        tooltip_border_radius=20
                        )

    chart3.add("Limpeza", 500)
    chart3.add("Funcionarios", 500)
    chart3.add("Utensílios", 500)

    grafico3 = chart3.render_data_uri()

    return grafico3


def reports():
    return render_template("reports.html")
