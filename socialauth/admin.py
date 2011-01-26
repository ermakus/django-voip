from socialauth.models import Profile, AuthMeta, OpenidProfile, TwitterUserProfile, FacebookUserProfile, LinkedInUserProfile

from django.contrib import admin

class ProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'creation_date')
    search_fields = ('name',)

admin.site.register(Profile, ProfileAdmin)

admin.site.register(AuthMeta)
admin.site.register(OpenidProfile)
admin.site.register(TwitterUserProfile)
admin.site.register(FacebookUserProfile)
admin.site.register(LinkedInUserProfile)
