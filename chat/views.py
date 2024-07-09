from django.shortcuts import render

# request: Objekt, wird standardmäßig in diese Funktion reingegeben
def index(request):
    return render(request, 'chat/index.html')

