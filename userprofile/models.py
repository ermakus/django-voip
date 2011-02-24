# coding=UTF-8
from django.db import models
from django.contrib.sites.models import Site
from django.contrib.auth.models import User
from django.template.defaultfilters import slugify
from django.utils.translation import ugettext as _
from django.template import loader, Context
from django.core.urlresolvers import reverse
from django.core.mail import send_mail
from django.conf import settings
from userprofile.countries import CountryField
from django.core.files.storage import default_storage

if hasattr(settings, "AWS_SECRET_ACCESS_KEY"):
    try:
        from backends.S3Storage import S3Storage
        storage = S3Storage()
    except ImportError:
        raise S3BackendNotFound
else:
    storage = default_storage

import datetime
import cPickle as pickle
import base64
import urllib
import os.path
try:
    from PIL import Image, ImageFilter
except ImportError:
    import Image, ImageFilter

AVATAR_SIZES = getattr(settings, 'AVATAR_SIZES', (128, 96, 64, 48, 32, 24, 16))
DEFAULT_AVATAR_SIZE = getattr(settings, 'DEFAULT_AVATAR_SIZE', 96)
if DEFAULT_AVATAR_SIZE not in AVATAR_SIZES:
    DEFAULT_AVATAR_SIZE = AVATAR_SIZES[0]
MIN_AVATAR_SIZE = getattr(settings, 'MIN_AVATAR_SIZE', DEFAULT_AVATAR_SIZE)
DEFAULT_AVATAR = getattr(settings, 'DEFAULT_AVATAR', os.path.join(settings.MEDIA_ROOT, "userprofile", "generic.jpg"))
DEFAULT_AVATAR_FOR_INACTIVES_USER = getattr(settings, 'DEFAULT_AVATAR_FOR_INACTIVES_USER', False)
# params to pass to the save method in PIL (dict with formats (JPEG, PNG, GIF...) as keys)
# see http://www.pythonware.com/library/pil/handbook/format-jpeg.htm and format-png.htm for options
SAVE_IMG_PARAMS = getattr(settings, 'SAVE_IMG_PARAMS', {})

class BaseProfile(models.Model):
    """
    User profile model
    """

    user = models.ForeignKey(User)
    creation_date = models.DateTimeField(default=datetime.datetime.now)
    country = CountryField(null=True, blank=True)
    latitude = models.DecimalField(max_digits=10, decimal_places=6, blank=True, null=True)
    longitude = models.DecimalField(max_digits=10, decimal_places=6, blank=True, null=True)
    location = models.CharField(max_length=255, blank=True, null=True)

    class Meta:
        abstract = True

    def has_avatar(self):
        return Avatar.objects.filter(user=self.user, valid=True).count()

    def __unicode__(self):
        return _("%s's profile") % self.user

    def get_absolute_url(self):
        return reverse("profile_public", args=[self.user])


class Avatar(models.Model):
    """
    Avatar model
    """
    image = models.ImageField(upload_to="avatars/%Y/%b/%d", storage=storage)
    user = models.ForeignKey(User)
    date = models.DateTimeField(auto_now_add=True)
    valid = models.BooleanField()

    class Meta:
        unique_together = (('user', 'valid'),)

    def __unicode__(self):
        return _("%s's Avatar") % self.user

    def delete(self):
        if hasattr(settings, "AWS_SECRET_ACCESS_KEY"):
            path = urllib.unquote(self.image.name)
        else:
            path = self.image.path

        base, filename = os.path.split(path)
        name, extension = os.path.splitext(filename)
        for key in AVATAR_SIZES:
            try:
                storage.delete(os.path.join(base, "%s.%s%s" % (name, key, extension)))
            except:
                pass

        super(Avatar, self).delete()

    def save(self, *args, **kwargs):
        for avatar in Avatar.objects.filter(user=self.user, valid=self.valid).exclude(id=self.id):
            if hasattr(settings, "AWS_SECRET_ACCESS_KEY"):
                path = urllib.unquote(self.image.name)
            else:
                path = avatar.image.path

            base, filename = os.path.split(path)
            name, extension = os.path.splitext(filename)
            for key in AVATAR_SIZES:
                try:
                    storage.delete(os.path.join(base, "%s.%s%s" % (name, key, extension)))
                except:
                    pass
            avatar.delete()

        super(Avatar, self).save(*args, **kwargs)


class EmailValidationManager(models.Manager):
    """
    Email validation manager
    """
    def verify(self, key):
        try:
            verify = self.get(key=key)
            if not verify.is_expired():
                verify.user.email = verify.email
                if hasattr(settings, "REQUIRE_EMAIL_CONFIRMATION") and settings.REQUIRE_EMAIL_CONFIRMATION:
                    verify.user.is_active = True
                verify.user.save()
                verify.verified = True
                verify.save()
                return True
            else:
                if not verify.verified:
                    verify.delete()
                return False
        except:
            return False

    def getuser(self, key):
        try:
            return self.get(key=key).user
        except:
            return False

    def add(self, user, email):
        """
        Add a new validation process entry
        """
        while True:
            key = User.objects.make_random_password(70)
            try:
                EmailValidation.objects.get(key=key)
            except EmailValidation.DoesNotExist:
                break

        template_body = "userprofile/email/validation.txt"
        template_subject = "userprofile/email/validation_subject.txt"
        site_name, domain = Site.objects.get_current().name, Site.objects.get_current().domain
        body = loader.get_template(template_body).render(Context(locals()))
        subject = loader.get_template(template_subject).render(Context(locals())).strip()
        send_mail(subject=subject, message=body, from_email=None, recipient_list=[email])
        user = User.objects.get(username=str(user))
        self.filter(user=user).delete()
        return self.create(user=user, key=key, email=email)

class EmailValidation(models.Model):
    """
    Email Validation model
    """
    user = models.ForeignKey(User, unique=True)
    email = models.EmailField(blank=True)
    key = models.CharField(max_length=70, unique=True, db_index=True)
    verified = models.BooleanField(default=False)
    created = models.DateTimeField(auto_now_add=True)
    objects = EmailValidationManager()

    def __unicode__(self):
        return _("Email validation process for %(user)s") % { 'user': self.user }

    def is_expired(self):
        if hasattr(settings, 'EMAIL_CONFIRMATION_DELAY'):
            expiration_delay = settings.EMAIL_CONFIRMATION_DELAY
        else:
            expiration_delay = 1
        return self.verified or \
            (self.created + datetime.timedelta(days=expiration_delay) <= datetime.datetime.now())

    def resend(self):
        """
        Resend validation email
        """
        template_body = "userprofile/email/validation.txt"
        template_subject = "userprofile/email/validation_subject.txt"
        site_name, domain = Site.objects.get_current().name, Site.objects.get_current().domain
        key = self.key
        body = loader.get_template(template_body).render(Context(locals()))
        subject = loader.get_template(template_subject).render(Context(locals())).strip()
        send_mail(subject=subject, message=body, from_email=None, recipient_list=[self.email])
        self.created = datetime.datetime.now()
        self.save()
        return True

class UserProfileMediaNotFound(Exception):
    pass

class S3BackendNotFound(Exception):
    pass

class GoogleDataAPINotFound(Exception):
    pass
