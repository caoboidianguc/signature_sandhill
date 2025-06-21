from django.contrib import admin
from .models import (Technician, Khach, Service, Chat, Like, TechWorkDay,
                     KhachVisit, Supply, Complimentary, ClientFavorite, OpiColor)
from simple_history.admin import SimpleHistoryAdmin

admin.site.register(Technician, SimpleHistoryAdmin)
admin.site.register(Chat)
admin.site.register(Like)
admin.site.register(Service)
admin.site.register(Khach, SimpleHistoryAdmin)
admin.site.register(TechWorkDay)
admin.site.register(KhachVisit)
admin.site.register(Supply)
admin.site.register(Complimentary)
admin.site.register(ClientFavorite)
admin.site.register(OpiColor)