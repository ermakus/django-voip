from django.contrib import admin
from asterisk.models import * 

class ChannelAdmin(admin.ModelAdmin):
    list_display = ("name","host","type","context","useragent","ipaddr","fullcontact",)

admin.site.register(Channel, ChannelAdmin)
