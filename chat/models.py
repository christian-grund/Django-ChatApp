from datetime import date, datetime
from django.conf import settings
from django.db import models

# Create your models here.

# models.Model: Django-Tabelle, Django baut Logik um Tabelle selbst
class Chat(models.Model):
    created_at = models.DateTimeField(default=datetime.now)

class Message(models.Model):
    text = models.CharField(max_length=500)
    created_at = models.DateTimeField(default=datetime.now)
    chat = models.ForeignKey(Chat, on_delete=models.CASCADE, related_name='chat_message_set', default=None, blank=True, null=True)
    author = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='author_message_set')
    receiver = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='receiver_message_set')

    # ForeignKey: wenn man auf anderes Objekt Referenzieren möchte. Ein ForeignKey in diesem Kontext bedeutet, dass jede Nachricht (Message) einem Benutzer zugeordnet ist, aber ein Benutzer mehrere Nachrichten haben kann.
    # settings.AUTH_USER_MODEL: Dies verweist auf das Benutzer-Modell, das in den Django-Einstellungen definiert ist. Standardmäßig ist dies das Modell User von Django, es könnte aber auch ein benutzerdefiniertes Benutzer-Modell sein, wenn dies in den Einstellungen (AUTH_USER_MODEL) so konfiguriert wurde.
    # on_delete=models.CASCADE: Dies definiert das Verhalten, wenn der verknüpfte Benutzer (Autor) gelöscht wird. models.CASCADE bedeutet, dass alle Nachrichten, die von diesem Benutzer erstellt wurden, ebenfalls gelöscht werden, wenn der Benutzer gelöscht wird. Es stellt sicher, dass keine verwaisten Nachrichten in der Datenbank verbleiben.
    # related_name='author_message_set': Dies gibt den Namen des Rückwärtsbezugs von der Benutzerinstanz zu den Nachrichten an. Anstatt den standardmäßigen Rückwärtsbezugsnamen zu verwenden (was message_set wäre), wird hier der Name author_message_set festgelegt. Das bedeutet, dass du von einem Benutzer-Objekt aus auf alle seine Nachrichten zugreifen kannst, indem du user.author_message_set.all() verwendest.
    # Zusammengefasst definiert diese Zeile also, dass jede Nachricht einen Autor hat, welcher ein Benutzer ist, und dass beim Löschen eines Benutzers alle seine Nachrichten ebenfalls gelöscht werden. Zudem kann man über den Rückwärtsbezug author_message_set von einem Benutzer aus alle seine Nachrichten abrufen.
    
