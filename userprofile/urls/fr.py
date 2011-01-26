from django.conf.urls.defaults import *
from django.views.generic.simple import direct_to_template
from userprofile.views import *
from django.conf import settings

urlpatterns = patterns('',
    # Private profile
    url(r'^profil/$', overview, name='profile_overview'),

    url(r'^profil/edition/localisation/$', location, name='profile_edit_location'),

    url(r'^profil/edition/informations/$', personal, name='profile_edit_personal'),

    url(r'^profil/suppression/$', delete, name='profile_delete'),

    url(r'^profil/recherche_pays/(?P<lat>[0-9\.\-]+)/(?P<lng>[0-9\.\-]+)/$',
        fetch_geodata,
        name='profile_geocountry_info'),

    # Avatars
    url(r'^profil/edition/avatar/suppression/$', avatardelete,
        name='profile_avatar_delete'),

    url(r'^profil/edition/avatar/$', avatarchoose, name='profile_edit_avatar'),

    url(r'^profil/edition/avatar/rognage/$', avatarcrop,
        name='profile_avatar_crop'),

    url(r'^profil/edition/avatar/rognage/fin/$', direct_to_template,
        { 'extra_context': {'section': 'avatar'},
        'template': 'userprofile/avatar/done.html'},
        name='profile_avatar_crop_done'),

    # Account utilities
    url(r'^email/validation/$', email_validation, name='email_validation'),

    url(r'^email/validation/fin/$', direct_to_template,
        {'template': 'userprofile/account/email_validation_processed.html'},
        name='email_validation_processed'),

    url(r'^email/validation/(?P<key>.{70})/$', email_validation_process,
        name='email_validation_process'),

    url(r'^email/validation/reinitialisation/$', email_validation_reset,
        name='email_validation_reset'),

    url(r'^email/validation/reinitialisation/(?P<action>done|failed)/$',
        direct_to_template,
        {'template' : 'userprofile/account/email_validation_reset_response.html'},
        name='email_validation_reset_response'),

    url(r'^motdepasse/reinitialisation/$', 'django.contrib.auth.views.password_reset',
        {'template_name': 'userprofile/account/password_reset.html',
         'email_template_name': 'userprofile/email/password_reset_email.txt' },
        name='password_reset'),

    url(r'^motdepasse/reinitialisation/fin/$',
        'django.contrib.auth.views.password_reset_done',
        {'template_name': 'userprofile/account/password_reset_done.html'},
        name='password_reset_done'),

    url(r'^motdepasse/modification/$', 'django.contrib.auth.views.password_change',
        {'template_name': 'userprofile/account/password_change.html'},
        name='password_change'),

    url(r'^motdepasse/modification/fin/$',
        'django.contrib.auth.views.password_change_done',
        {'template_name': 'userprofile/account/password_change_done.html'},
        name='password_change_done'),

    url(r'^reinitialisation/(?P<uidb36>[0-9A-Za-z]+)-(?P<token>.+)/$',
        'django.contrib.auth.views.password_reset_confirm',
        {'template_name': 'userprofile/account/password_reset_confirm.html'},
        name="password_reset_confirm"),

    url(r'^reinitialisation/fin/$',
        'django.contrib.auth.views.password_reset_complete',
        {'template_name': 'userprofile/account/password_reset_complete.html'},
        name="password_reset_complete"),

    url(r'^connexion/$', 'django.contrib.auth.views.login',
        {'template_name': 'userprofile/account/login.html'},
        name='login'),

    url(r'^deconnexion/$', 'django.contrib.auth.views.logout',
        {'template_name': 'userprofile/account/logout.html'},
        name='logout'),

    # Registration
    url(r'^enregistrement/$', register, name='signup'),

    url(r'^enegistrement/validation/$', direct_to_template,
        {'template' : 'userprofile/account/validate.html'},
        name='signup_validate'),

    url(r'^enregistrement/fin/$', direct_to_template,
        {'extra_context': { 'email_validation_required': hasattr(settings, "REQUIRE_EMAIL_CONFIRMATION") and settings.REQUIRE_EMAIL_CONFIRMATION },
         'template': 'userprofile/account/registration_done.html'},
        name='signup_complete'),

    # Users public profile
    url(r'^profil/(?P<username>.+)/$', public, name='profile_public'),

)
