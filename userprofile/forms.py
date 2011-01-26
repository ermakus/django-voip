from django import forms
from django.core.exceptions import ObjectDoesNotExist
from django.core.exceptions import ImproperlyConfigured
from django.db import models
from django.utils.translation import ugettext as _
from django.conf import settings
from django.contrib.auth.models import User, SiteProfileNotAvailable
from userprofile.models import EmailValidation, AVATAR_SIZES, DEFAULT_AVATAR_SIZE, MIN_AVATAR_SIZE
from django.core.files.uploadedfile import SimpleUploadedFile
import mimetypes, urllib
from django.contrib.auth.forms import UserCreationForm

if not settings.AUTH_PROFILE_MODULE:
    raise SiteProfileNotAvailable
try:
    app_label, model_name = settings.AUTH_PROFILE_MODULE.split('.')
    Profile = models.get_model(app_label, model_name)
except (ImportError, ImproperlyConfigured):
    raise SiteProfileNotAvailable

class LocationForm(forms.ModelForm):
    """
    Profile location form
    """

    class Meta:
        model = Profile
        fields = ('location', 'latitude', 'longitude', 'country')

class ProfileForm(forms.ModelForm):
    """
    Profile Form. Composed by all the Profile model fields.
    """
    class Meta:
        model = Profile
        exclude = ('creation_date', 'location', 'latitude', 'longitude', 'country',
                   'user', 'public', 'site')

class PublicFieldsForm(forms.ModelForm):
    """
    Public Fields of the Profile Form. Composed by all the Profile model fields.
    """
    class Meta:
        model = Profile
        exclude = ('creation_date', 'user', 'public')

class AvatarForm(forms.Form):
    """
    The avatar form requires only one image field.
    """
    photo = forms.ImageField(required=False, help_text=_("Select an image from disk"))
    url = forms.URLField(required=False, help_text=_("Select an image from a remote URL. Put the URL on the input below and we'll retrieve the image for you"))

    def clean_url(self):
        url = self.cleaned_data.get('url')
        if not url: return ''
        try:
            filename, headers = urllib.urlretrieve(url)
        except:
            raise forms.ValidationError(forms.fields.URLField.default_error_messages['invalid_link'])
        if not mimetypes.guess_all_extensions(headers.get('Content-Type')):
            raise forms.ValidationError(_('The file type is invalid: %s' % type))
        return SimpleUploadedFile(filename, open(filename).read(), content_type=headers.get('Content-Type'))

    def clean(self):
        if not (self.cleaned_data.get('photo') or self.cleaned_data.get('url')):
            raise forms.ValidationError(_('You must enter one of the options'))
        return self.cleaned_data

class AvatarCoordinateField(forms.IntegerField):
    def clean(self, value):
        try:
            value = int(float(value))
        except:
            pass
        return super(AvatarCoordinateField, self).clean(value)

class AvatarCropForm(forms.Form):
    """
    Crop dimensions form
    """
    top = AvatarCoordinateField()
    bottom = AvatarCoordinateField()
    left = AvatarCoordinateField()
    right = AvatarCoordinateField()

    def __init__(self, image=None, *args, **kwargs):
        self.image = image
        super(AvatarCropForm, self).__init__(*args, **kwargs)

    def clean(self):
        if self.cleaned_data.get('right') and self.cleaned_data.get('left') and \
           int(self.cleaned_data.get('right')) - int(self.cleaned_data.get('left')) < MIN_AVATAR_SIZE:
            raise forms.ValidationError(_("You must select a portion of the image with a minimum of %(min_avatar_size)dx%(min_avatar_size)d pixels.") % { 'min_avatar_size': MIN_AVATAR_SIZE })

        return self.cleaned_data



class RegistrationForm(UserCreationForm):
    email = forms.EmailField(required=getattr(settings, "REQUIRE_EMAIL_CONFIRMATION", False), label=_("E-mail address"))

    class Meta:
        model = User
        fields = ("username","email",)

    def clean_email(self):
        """
        Verify that the email exists
        """
        email = self.cleaned_data.get("email")

        if not email: return  email

        try:
            User.objects.get(email__iexact=email)
            raise forms.ValidationError(_("That e-mail is already used."))
        except User.DoesNotExist:
            try:
                EmailValidation.objects.get(email=email)
                raise forms.ValidationError(_("That e-mail is already being confirmed."))
            except EmailValidation.DoesNotExist:
                return email

    def save(self, *args, **kwargs):
        user = super(RegistrationForm, self).save(commit=False)
        user.is_active = not getattr(settings, "REQUIRE_EMAIL_CONFIRMATION", False)
        user.save()
        if self.cleaned_data.get('email'):
            EmailValidation.objects.add(user=user, email=user.email)
        return user

try:
    _temp = settings.REGISTRATION_FORM.split('.')
    _form_class = _temp.pop()
    _module = __import__('.'.join(_temp), globals(), locals(), [_form_class])
    _RegistrationForm = getattr(_module, _form_class)
except:
    _RegistrationForm = RegistrationForm

class EmailValidationForm(forms.Form):
    email = forms.EmailField()

    def clean_email(self):
        """
        Verify that the email exists
        """
        email = self.cleaned_data.get("email")
        if not (User.objects.filter(email=email) or EmailValidation.objects.filter(email=email)):
            return email

        raise forms.ValidationError(_("That e-mail is already used."))

class ResendEmailValidationForm(forms.Form):
    email = forms.EmailField()

    def clean_email(self):
        """
        Verify that the email exists
        """
        email = self.cleaned_data.get("email")
        if User.objects.filter(email=email) or EmailValidation.objects.filter(email=email):
            return email

        raise forms.ValidationError(_("That e-mail isn't registered."))
