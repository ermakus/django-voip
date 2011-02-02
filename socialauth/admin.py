from socialauth.models import Profile

from django.contrib import admin

class ProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'creation_date')
    search_fields = ('name',)

admin.site.register(Profile, ProfileAdmin)
