from django.shortcuts import render


# Create your views here.
def home(request):

    processos = extrai_processos()

    return render(request, 'extrator/home.html', {'processos': processos})