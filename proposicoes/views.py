from django.shortcuts import render
from datetime import datetime
import requests
import pandas as pd
import json

# Create your views here.

def RenderProposicoes(request, year=datetime.now().year):
    """
        View function for home page of Proposições.
    """

    data = GetProposicoes(year)
    context = {
        "data" : data,
        "years" : range(datetime.now().year, 1984, -1),
    }

    if request.method == "POST":
        year = request.POST.get("select_year")
        data = GetProposicoes(year)
        context["data"] = data
        context["data_len"] = range(len(data))
        context["year"] = year
        return render(request, "proposicoes.html", context=context)
    else:
        return render(request, "proposicoes.html", context=context)

def GetProposicoes(year):
    """
        Get data from Dados Abertos Câmara dos Deputados from selected year
    """
    url = f"http://dadosabertos.camara.leg.br/arquivos/proposicoes/json/proposicoes-{year}.json"
    response = requests.get(url)
    if response.status_code == 200:
        df = pd.json_normalize(response.json()["dados"])
        df = df[["id", "uri", "siglaTipo", "ementa", "descricaoTipo"]]
        df = df.assign(Tipo = df.descricaoTipo.astype(str) + " (" + df.siglaTipo + ")")
        df = df.drop(columns=["siglaTipo", "descricaoTipo"])
        return df
    else:
        return response.raise_for_status()
