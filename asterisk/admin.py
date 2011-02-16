from django.contrib import admin
from asterisk.models import * 

class PeersAdmin(admin.ModelAdmin):
    list_display = ("name","host","type","context","useragent","ipaddr","fullcontact",)

admin.site.register(Peers, PeersAdmin)
