from django.contrib import admin
from .models import Chat, Message

class MessageAdmin(admin.ModelAdmin):
    fields = ('chat', 'text', 'created_at', 'author', 'receiver')           # Ansicht der Felder, die in der Detailansicht der Message angezeigt werden (z.B. nur für bestimmte Admins sichtbar)
    list_display = ('text', 'author', 'receiver', 'created_at')     # Anzeige der Spalten in der Chat-Übersicht
    search_fields = ('text',)                                       # Zum Filtern nach einer Kategorie

# Register your models here.
admin.site.register(Message, MessageAdmin)
admin.site.register(Chat)