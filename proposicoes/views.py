from django.shortcuts import render
import requests
import pandas as pd
import json

# Create your views here.

def index(request):
    """View function for home page of site."""


    response = requests.get("https://dadosabertos.camara.leg.br/arquivos/proposicoes/json/proposicoes-2022.json")
    response = response.json()["dados"]
    proposicoes_df = pd.json_normalize(response)
    data = proposicoes_df.to_json()
    data = json.loads(data)

    # # Generate counts of some of the main objects
    # num_books = Book.objects.all().count()
    # num_instances = BookInstance.objects.all().count()

    # # Available books (status = 'a')
    # num_instances_available = BookInstance.objects.filter(status__exact='a').count()

    # # The 'all()' is implied by default.
    # num_authors = Author.objects.count()

    # context = {
    #     'num_books': num_books,
    #     'num_instances': num_instances,
    #     'num_instances_available': num_instances_available,
    #     'num_authors': num_authors,
    # }

    context = {
        "data" : proposicoes_df,
        "range" : range(len(proposicoes_df)),
    }

    # Render the HTML template index.html with the data in the context variable
    return render(request, 'index.html', context=context)
