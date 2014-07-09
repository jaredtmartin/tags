from django.db import models
from django.contrib.auth.models import BaseUserManager, AbstractBaseUser


class UserManager(BaseUserManager):
    def create_user(self, email, password=None, phone = None, first_name = ''):
        """
        Creates and saves a User with the given email, date of
        birth and password.
        """
        if not email:
            raise ValueError('Users must have an email address')

        user = self.model(
            email=self.normalize_email(email),
        )

        user.set_password(password)
        if phone: user.phone = phone
        if first_name: user.first_name = first_name
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password):
        """
        Creates and saves a superuser with the given email, date of
        birth and password.
        """
        user = self.create_user(email,
            password=password,
        )
        user.is_admin = True
        user.save(using=self._db)
        return user

class User(AbstractBaseUser):
    email = models.EmailField(verbose_name='Email Address', max_length=255, unique=True, db_index=True,)
    first_name = models.CharField('First Name', max_length=30, blank=True)
    last_name = models.CharField('Last Name', max_length=30, blank=True)
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
    is_active = models.BooleanField(default=True)
    is_admin = models.BooleanField(default=False)
    is_retailer = models.BooleanField(default=False)
    use_nominee = models.BooleanField(default=False)
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
    objects = UserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    def get_full_name(self):
        # The user is identified by their email address
        return "%s %s" % (self.first_name, self.last_name)
    full_name = property(get_full_name)
    def get_short_name(self):
        # The user is identified by their email address
        return self.first_name

    # On Python 3: def __str__(self):
    def __unicode__(self):
        return "%s %s" % (self.first_name, self.last_name)

    def has_perm(self, perm, obj=None):
        "Does the user have a specific permission?"
        # Simplest possible answer: Yes, always
        return True

    def has_module_perms(self, app_label):
        "Does the user have permissions to view the app `app_label`?"
        # Simplest possible answer: Yes, always
        return True

    @property
    def is_staff(self):
        "Is the user a member of staff?"
        # Simplest possible answer: All admins are staff
        return self.is_admin