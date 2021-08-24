from django.contrib import admin

from .models import ConnectionsLogs, Investigator, Codes


admin.site.register(ConnectionsLogs)
admin.site.register(Investigator)
admin.site.register(Codes)
