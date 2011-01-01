from socialauth.models import AuthMeta, OpenidProfile, TwitterUserProfile, FacebookUserProfile, KinopoiskUserProfile, LinkedInUserProfile

from django.contrib import admin

admin.site.register(AuthMeta)
admin.site.register(OpenidProfile)
admin.site.register(KinopoiskUserProfile)
admin.site.register(TwitterUserProfile)
admin.site.register(FacebookUserProfile)
admin.site.register(LinkedInUserProfile)
