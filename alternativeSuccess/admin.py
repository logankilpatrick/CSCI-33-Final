from django.contrib import admin

from .models import User, Program, School, Message

admin.site.register(User)
admin.site.register(Program)
admin.site.register(School)
admin.site.register(Message)

