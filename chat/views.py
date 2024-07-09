from django.shortcuts import render
from .models import Chat, Message

# request: Objekt, wird standardmäßig in diese Funktion reingegeben
def index(request):
    if request.method == 'POST':
        print("Received data: " + request.POST['textmessage'])
        myChat = Chat.objects.get(id=1)
        Message.objects.create(text=request.POST['textmessage'], chat=myChat, author=request.user, receiver=request.user)                              # Nachricht wird erstellt
    return render(request, 'chat/index.html', {'username': 'Christian'})

