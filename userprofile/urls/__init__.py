from django.conf import settings

try:
    if not hasattr(settings, "I18N_URLS") or not settings.I18N_URLS \
                                          or not settings.LANGUAGE_CODE:
        raise

    try:
        module = __import__("userprofile.urls.%s" % (settings.LANGUAGE_CODE), \
                            {}, {}, "urlpatterns")
    except:
        module = __import__( \
            "userprofile.urls.%s" % (settings.LANGUAGE_CODE.split('-')[0]), \
            {}, {}, "urlpatterns")

except:
    module = __import__("userprofile.urls.en", {}, {}, "urlpatterns")

globals().update({ "urlpatterns": module.__dict__["urlpatterns"] })
