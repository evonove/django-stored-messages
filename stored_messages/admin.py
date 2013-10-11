from django.contrib import admin
from .models import Inbox, Message, MessageArchive


admin.site.register(Inbox)
admin.site.register(Message)
admin.site.register(MessageArchive)
