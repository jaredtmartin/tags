from django.db import models
from django.contrib.auth.models import BaseUserManager, AbstractBaseUser


class UserManager(BaseUserManager):
    def create_user(self, email, password=None):
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
    email = models.EmailField(
        verbose_name='email address',
        max_length=255,
        unique=True,
        db_index=True,
    )
    first_name = models.CharField('first name', max_length=30, blank=True)
    last_name = models.CharField('last name', max_length=30, blank=True)
    street = models.CharField('street address', max_length=32, blank=True, default="")
    city = models.CharField('city', max_length=32, blank=True, default="")
    state = models.CharField('state', max_length=32, blank=True, default="")
    phone = models.CharField('phone number', max_length=16, blank=True, default="")
    phone2 = models.CharField('alternate phone number', max_length=16, blank=True, default="")
    email2 = models.CharField('alternate email', max_length=16, blank=True, default="")
    country = models.CharField('country', max_length=16, blank=True, default="")
    timezone = models.CharField('timezone', max_length=16, blank=True, default="")
    is_active = models.BooleanField(default=True)
    is_admin = models.BooleanField(default=False)
    use_nominee = models.BooleanField(default=False)
    nominee_first_name = models.CharField('nominee first name', max_length=30, blank=True)
    nominee_last_name = models.CharField('nominee last name', max_length=30, blank=True)
    nominee_street = models.CharField('nominee street address', max_length=32, blank=True, default="")
    nominee_city = models.CharField('nominee city', max_length=32, blank=True, default="")
    nominee_state = models.CharField('nominee state', max_length=32, blank=True, default="")
    nominee_phone = models.CharField('nominee phone number', max_length=16, blank=True, default="")
    nominee_phone2 = models.CharField('nominee alternate phone number', max_length=16, blank=True, default="")
    nominee_email = models.CharField('nominee email', max_length=16, blank=True, default="")
    nominee_email2 = models.CharField('nominee alternate email', max_length=16, blank=True, default="")
    nominee_country = models.CharField('nominee_country', max_length=16, blank=True, default="")
    nominee_timezone = models.CharField('nominee_timezone', max_length=16, blank=True, default="")
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