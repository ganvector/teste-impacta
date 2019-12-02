from django.shortcuts import render
from django.http import HttpResponse
from django.views.generic import View
from django.core.files.storage import FileSystemStorage

from .extract import extrai_processos

DATA_FOLDER = 'avaliacao/extrator/data/'

class Home(View):
    template_name = 'extrator/home.html'

    def post(self, request, *args, **kwargs):
        arquivo = request.FILES['pagina']
        context = {}
        fs = FileSystemStorage(location=DATA_FOLDER)

        filename = fs.save(arquivo.name, arquivo)

        context['processos'] = extrai_processos()

        return render(request, self.template_name, context)

    def get(self, request, *args, **kwargs):
        context = {}

        context['processos'] = extrai_processos()

        return render(request, self.template_name, context)
