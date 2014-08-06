from django.db import models
# from django.contrib.auth.models import BaseUserManager, AbstractBaseUser


# class UserManager(BaseUserManager):
#     def create_user(self, email, password=None, phone = None, first_name = '', force_change_password = False):
#         """
#         Creates and saves a User with the given email, date of
#         birth and password.
#         """
#         if not email:
#             raise ValueError('Users must have an email address')

#         user = self.model(
#             email=self.normalize_email(email),
#         )

#         user.set_password(password)
#         if phone: user.phone = phone
#         if first_name: user.first_name = first_name
#         user.force_change_password = force_change_password
#         user.save(using=self._db)
#         return user

#     def create_superuser(self, email, password):
#         """
#         Creates and saves a superuser with the given email, date of
#         birth and password.
#         """
#         user = self.create_user(email,
#             password=password,
#         )
#         user.is_admin = True
#         user.save(using=self._db)
#         return user
from django.contrib.auth import models as django_models
# class User(django_user_models.AbstractUser):
#     street = models.CharField('Street Address', max_length=32, blank=True, default="")
#     city = models.CharField('City', max_length=32, blank=True, default="")
#     state = models.CharField('State', max_length=32, blank=True, default="")
#     phone = models.CharField('Phone number', max_length=16, blank=True, default="")
#     phone2 = models.CharField('Alternate phone number', max_length=16, blank=True, default="")
#     email2 = models.CharField('Alternate email', max_length=255, blank=True, default="")
#     country = models.CharField('Country', max_length=16, blank=True, default="")
#     timezone = models.CharField('Timezone', max_length=16, blank=True, default="")
#     security_question = models.CharField('Security Question', max_length=255, blank=True, default="")
#     security_response = models.CharField('Security Response', max_length=255, blank=True, default="")
#     dob = models.CharField('Date of Birth', max_length=16, blank=True, default="")
#     is_retailer = models.BooleanField(default=False)
#     use_nominee = models.BooleanField(default=False)
#     force_change_password = models.BooleanField(default=False)
#     nominee_first_name = models.CharField('Nominee First Name', max_length=30, blank=True)
#     nominee_last_name = models.CharField('Nominee Last Name', max_length=30, blank=True)
#     nominee_street = models.CharField('Nominee street address', max_length=32, blank=True, default="")
#     nominee_city = models.CharField('Nominee City', max_length=32, blank=True, default="")
#     nominee_state = models.CharField('Nominee State', max_length=32, blank=True, default="")
#     nominee_phone = models.CharField('Nominee Phone number', max_length=16, blank=True, default="")
#     nominee_phone2 = models.CharField('Nominee Alternate phone number', max_length=16, blank=True, default="")
#     nominee_email = models.CharField('Nominee email', max_length=255, blank=True, default="")
#     nominee_email2 = models.CharField('Nominee Alternate email', max_length=16, blank=True, default="")
#     nominee_country = models.CharField('Nominee_country', max_length=255, blank=True, default="")
#     nominee_timezone = models.CharField('Nominee_timezone', max_length=16, blank=True, default="")
#     REQUIRED_FIELDS = []

from django.utils.translation import ugettext_lazy as _
from django.core import validators
import re
from django.utils import timezone
class User(django_models.AbstractBaseUser, django_models.PermissionsMixin):
    """
    An abstract base class implementing a fully featured User model with
    admin-compliant permissions.

    Username, password and email are required. Other fields are optional.
    """
    username = models.CharField(_('username'), max_length=30, unique=True,
        help_text=_('Required. 30 characters or fewer. Letters, numbers and '
                    '@/./+/-/_ characters'),
        validators=[
            validators.RegexValidator(re.compile('^[\w.@+-]+$'), _('Enter a valid username.'), 'invalid')
        ])
    first_name = models.CharField(_('first name'), max_length=30, blank=True)
    last_name = models.CharField(_('last name'), max_length=30, blank=True)
    email = models.EmailField(_('email address'), blank=True)
    is_staff = models.BooleanField(_('staff status'), default=False,
        help_text=_('Designates whether the user can log into this admin '
                    'site.'))
    is_active = models.BooleanField(_('active'), default=True,
        help_text=_('Designates whether this user should be treated as '
                    'active. Unselect this instead of deleting accounts.'))
    date_joined = models.DateTimeField(_('date joined'), default=timezone.now)



    street = models.CharField('Street Address', max_length=32, blank=True, default="")
    city = models.CharField('City', max_length=32, blank=True, default="")
    state = models.CharField('State', max_length=32, blank=True, default="")
    phone = models.CharField('Phone number', max_length=16, blank=True, default="")
    phone2 = models.CharField('Alternate phone number', max_length=16, blank=True, default="")
    email2 = models.CharField('Alternate email', max_length=255, blank=True, default="")
    country = models.CharField('Country', max_length=16, blank=True, default="")
    timezone = models.CharField('Timezone', max_length=16, blank=True, default="")
    security_question = models.CharField('Security Question', max_length=255, blank=True, default="")
    security_response = models.CharField('Security Response', max_length=255, blank=True, default="")
    dob = models.CharField('Date of Birth', max_length=16, blank=True, default="")
    is_retailer = models.BooleanField(default=False)
    use_nominee = models.BooleanField(default=False)
    blocked_until = models.DateTimeField(_('blocked_until'), default=None, blank=True, null=True)
    tries_left = models.IntegerField(default=3)
    force_change_password = models.BooleanField(default=False)
    nominee_first_name = models.CharField('Nominee First Name', max_length=30, blank=True)
    nominee_last_name = models.CharField('Nominee Last Name', max_length=30, blank=True)
    nominee_street = models.CharField('Nominee street address', max_length=32, blank=True, default="")
    nominee_city = models.CharField('Nominee City', max_length=32, blank=True, default="")
    nominee_state = models.CharField('Nominee State', max_length=32, blank=True, default="")
    nominee_phone = models.CharField('Nominee Phone number', max_length=16, blank=True, default="")
    nominee_phone2 = models.CharField('Nominee Alternate phone number', max_length=16, blank=True, default="")
    nominee_email = models.CharField('Nominee email', max_length=255, blank=True, default="")
    nominee_email2 = models.CharField('Nominee Alternate email', max_length=16, blank=True, default="")
    nominee_country = models.CharField('Nominee_country', max_length=255, blank=True, default="")
    nominee_timezone = models.CharField('Nominee_timezone', max_length=16, blank=True, default="")


    objects = django_models.UserManager()

    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = ['email']

    class Meta:
        verbose_name = _('user')
        verbose_name_plural = _('users')

    def get_absolute_url(self):
        return "/users/%s/" % urlquote(self.username)

    def get_full_name(self):
        """
        Returns the first_name plus the last_name, with a space in between.
        """
        full_name = '%s %s' % (self.first_name, self.last_name)
        return full_name.strip()

    def get_short_name(self):
        "Returns the short name for the user."
        return self.first_name

    def email_user(self, subject, message, from_email=None):
        """
        Sends an email to this User.
        """
        send_mail(subject, message, from_email, [self.email])

    def get_profile(self):
        """
        Returns site-specific profile for this user. Raises
        SiteProfileNotAvailable if this site does not allow profiles.
        """
        warnings.warn("The use of AUTH_PROFILE_MODULE to define user profiles has been deprecated.",
            PendingDeprecationWarning)
        if not hasattr(self, '_profile_cache'):
            from django.conf import settings
            if not getattr(settings, 'AUTH_PROFILE_MODULE', False):
                raise SiteProfileNotAvailable(
                    'You need to set AUTH_PROFILE_MODULE in your project '
                    'settings')
            try:
                app_label, model_name = settings.AUTH_PROFILE_MODULE.split('.')
            except ValueError:
                raise SiteProfileNotAvailable(
                    'app_label and model_name should be separated by a dot in '
                    'the AUTH_PROFILE_MODULE setting')
            try:
                model = models.get_model(app_label, model_name)
                if model is None:
                    raise SiteProfileNotAvailable(
                        'Unable to load the profile model, check '
                        'AUTH_PROFILE_MODULE in your project settings')
                self._profile_cache = model._default_manager.using(
                                   self._state.db).get(user__id__exact=self.id)
                self._profile_cache.user = self
            except (ImportError, ImproperlyConfigured):
                raise SiteProfileNotAvailable
        return self._profile_cache
class PhoneNumber(models.Model):
    blocked_until = models.DateTimeField(_('blocked_until'), default=None, blank=True, null=True)
    tries_left = models.IntegerField(default=3)
    phone = models.CharField('Phone number', max_length=16, blank=True, default="")