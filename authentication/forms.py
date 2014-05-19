from django.contrib.sites.models import Site
# from django.contrib.auth.models import User
from authentication.models import User
from django.contrib.auth.tokens import default_token_generator
from django.contrib.auth import forms as django_forms
from django.utils.http import int_to_base36
# from articles.widgets import BootstrapDropdown
from django.forms import widgets
from django.template import Context, loader
from django.conf import settings
from django import forms
import pytz
from django.core.mail import send_mail
from django.forms import ModelForm, ChoiceField
# from articles.models import UserProfile, USER_MODES
class SimpleUserCreationForm(forms.ModelForm):
    password1 = forms.CharField(label="Password", widget=forms.PasswordInput(attrs={'placeholder':'Password','class':'form-control'}))
    password2 = forms.CharField(label="Password confirmation", widget=forms.PasswordInput(attrs={'placeholder':'Retype Password','class':'form-control'}),
                                help_text = "Enter the same password as above, for verification.")
    email = forms.EmailField(label="Email", max_length=75, widget=widgets.TextInput(attrs={'placeholder':'E-mail address','class':'form-control'}))

    class Meta:
        model = User
        fields = set()

    def clean_password2(self):
        password1 = self.cleaned_data.get("password1", "")
        password2 = self.cleaned_data["password2"]
        if password1 != password2:
            raise forms.ValidationError("The two password fields didn't match.")
        return password2
    
    def clean_email1(self):
        email = self.cleaned_data["email"]
        users_found = User.objects.filter(email__iexact=email)
        if len(users_found) >= 1:
            raise forms.ValidationError("A user with that email already exist.")
        return email

    def save(self, commit=True, domain_override=None,
             email_template_name='registration/signup_email.html',
             use_https=False, token_generator=default_token_generator):
        user = super(SimpleUserCreationForm, self).save(commit=False)
        user.set_password(self.cleaned_data["password1"])
        user.email = self.cleaned_data["email"]
        user.username = self.cleaned_data["email"]
        user.is_active = False
        if commit:
            user.save()
        if not domain_override:
            current_site = Site.objects.get_current()
            site_name = current_site.name
            domain = current_site.domain
        else:
            site_name = domain = domain_override
        t = loader.get_template(email_template_name)
        c = {
            'email': user.email,
            'domain': domain,
            'site_name': site_name,
            'uid': int_to_base36(user.id),
            'user': user,
            'token': token_generator.make_token(user),
            'protocol': use_https and 'https' or 'http',
            }
        send_mail("Confirmation link sent on %s" % site_name,
                  t.render(Context(c)), settings.EMAIL_HOST_USER, [user.email])
        return user
class SimpleUserCreationFormWithFullName(SimpleUserCreationForm):
    class Meta:
        model = User
        fields = ("first_name","last_name")
    first_name = forms.CharField(label="First Name", widget=forms.TextInput(attrs={'placeholder':'First Name','class':'form-control'}))
    last_name = forms.CharField(label="Last Name", widget=forms.TextInput(attrs={'placeholder':'Last Name','class':'form-control'}))
    email2 = forms.CharField(label="Alternative Email", widget=forms.TextInput(attrs={'placeholder':'Alternative Email','class':'form-control'}))

# class UserCreationForm(forms.ModelForm):
#     username = forms.RegexField(label="Username", max_length=30, regex=r'^[\w.@+-]+$',
#                                 help_text="Required. 30 characters or fewer. Letters, digits and @/./+/-/_ only.",
#                                 error_messages = {'invalid': "This value may contain only letters, numbers and @/./+/-/_ characters."})
#     password1 = forms.CharField(label="Password", widget=forms.PasswordInput)
#     password2 = forms.CharField(label="Password confirmation", widget=forms.PasswordInput,
#                                 help_text = "Enter the same password as above, for verification.")
#     email1 = forms.EmailField(label="Email", max_length=75)
#     email2 = forms.EmailField(label="Email confirmation", max_length=75,
#                               help_text = "Enter your email address again. A confirmation email will be sent to this address.")

#     class Meta:
#         model = User
#         fields = ("username",)

#     def clean_password2(self):
#         password1 = self.cleaned_data.get("password1", "")
#         password2 = self.cleaned_data["password2"]
#         if password1 != password2:
#             raise forms.ValidationError("The two password fields didn't match.")
#         return password2
    
#     def clean_email1(self):
#         email1 = self.cleaned_data["email1"]
#         users_found = User.objects.filter(email__iexact=email1)
#         if len(users_found) >= 1:
#             raise forms.ValidationError("A user with that email already exist.")
#         return email1

#     def clean_email2(self):
#         email1 = self.cleaned_data.get("email1", "")
#         email2 = self.cleaned_data["email2"]
#         if email1 != email2:
#             raise forms.ValidationError("The two email fields didn't match.")
#         return email2

#     def save(self, commit=True, domain_override=None,
#              email_template_name='registration/signup_email.html',
#              use_https=False, token_generator=default_token_generator):
#         user = super(UserCreationForm, self).save(commit=False)
#         user.set_password(self.cleaned_data["password1"])
#         user.email = self.cleaned_data["email1"]
#         user.is_active = False
#         if commit:
#             user.save()
#         if not domain_override:
#             current_site = Site.objects.get_current()
#             site_name = current_site.name
#             domain = current_site.domain
#         else:
#             site_name = domain = domain_override
#         t = loader.get_template(email_template_name)
#         c = {
#             'email': user.email,
#             'domain': domain,
#             'site_name': site_name,
#             'uid': int_to_base36(user.id),
#             'user': user,
#             'token': token_generator.make_token(user),
#             'protocol': use_https and 'https' or 'http',
#             }
#         send_mail("Confirmation link sent on %s" % site_name,
#                   t.render(Context(c)), 'peyman.gohari@gmail.com', [user.email])
#         return user

def get_timezone_choices():
        return [(t,t) for t in pytz.common_timezones]
class UserForm(ModelForm):
  class Meta:
    model = User
    fields = ('first_name','last_name','email', 'street','city','state','phone', 'email2', 'phone2','use_nominee', 'nominee_first_name', 'nominee_last_name', 'nominee_email', 'nominee_email2', 'nominee_street', 'nominee_city', 
        'nominee_state', 'nominee_phone', 'nominee_phone2')
  first_name = forms.CharField(label="First Name", max_length=30, widget=widgets.TextInput(attrs={'placeholder':'First Name','class':'form-control'}))
  last_name = forms.CharField(label="Last Name", max_length=30, widget=widgets.TextInput(attrs={'placeholder':'Last Name','class':'form-control'}))
  email = forms.CharField(label="Email Address", max_length=30, widget=widgets.TextInput(attrs={'placeholder':'Email Address','class':'form-control'}))
  email2 = forms.CharField(label="Alternate Email Address", required=False, max_length=30, widget=widgets.TextInput(attrs={'placeholder':'Alternate Email','class':'form-control'}))
  street = forms.CharField(label="Street Address", required=False, max_length=30, widget=widgets.TextInput(attrs={'placeholder':'Street Address','class':'form-control'}))
  city = forms.CharField(label="City", required=False, max_length=30, widget=widgets.TextInput(attrs={'placeholder':'City','class':'form-control'}))
  state = forms.CharField(label="State", required=False, max_length=30, widget=widgets.TextInput(attrs={'placeholder':'State','class':'form-control'}))
  phone = forms.CharField(label="Phone", required=False, max_length=30, widget=widgets.TextInput(attrs={'placeholder':'Phone','class':'form-control'}))
  phone2 = forms.CharField(label="Second Phone", required=False, max_length=30, widget=widgets.TextInput(attrs={'placeholder':'Second Phone','class':'form-control'}))

  use_nominee = forms.BooleanField(label="Use Nominee", required=False, widget=widgets.CheckboxInput(attrs={'placeholder':'Use Nominee','data-toggle':"checkbox"}))
  nominee_first_name = forms.CharField(label="First Name", required=False, max_length=30, widget=widgets.TextInput(attrs={'placeholder':'First Name','class':'form-control'}))
  nominee_last_name = forms.CharField(label="Last Name", required=False, max_length=30, widget=widgets.TextInput(attrs={'placeholder':'Last Name','class':'form-control'}))
  nominee_email = forms.CharField(label="Email Address", required=False, max_length=30, widget=widgets.TextInput(attrs={'placeholder':'Email Address','class':'form-control'}))
  nominee_email2 = forms.CharField(label="Alternate Email Address", required=False, max_length=30, widget=widgets.TextInput(attrs={'placeholder':'Alternate Email','class':'form-control'}))
  nominee_street = forms.CharField(label="Street Address", required=False, max_length=30, widget=widgets.TextInput(attrs={'placeholder':'Street Address','class':'form-control'}))
  nominee_city = forms.CharField(label="City", required=False, max_length=30, widget=widgets.TextInput(attrs={'placeholder':'City','class':'form-control'}))
  nominee_state = forms.CharField(label="State", required=False, max_length=30, widget=widgets.TextInput(attrs={'placeholder':'State','class':'form-control'}))
  nominee_phone = forms.CharField(label="Phone", required=False, max_length=30, widget=widgets.TextInput(attrs={'placeholder':'Phone','class':'form-control'}))
  nominee_phone2 = forms.CharField(label="Second Phone", required=False, max_length=30, widget=widgets.TextInput(attrs={'placeholder':'Second Phone','class':'form-control'}))


class LoginForm(django_forms.AuthenticationForm):
    username = forms.CharField(label="E-mail", max_length=30, widget=widgets.TextInput(attrs={'placeholder':'E-mail address','class':'form-control'}))
    password = forms.CharField(label="Password", widget=forms.PasswordInput(attrs={'placeholder':'Password','class':'form-control'}))

class PasswordResetForm(django_forms.PasswordResetForm):
    email = forms.EmailField(label="E-mail", max_length=75, widget=widgets.TextInput(attrs={'placeholder':'E-mail address','class':'form-control'}))
class SetPasswordForm(django_forms.SetPasswordForm):
    new_password1 = forms.CharField(label="New password",
                                    widget=forms.PasswordInput(attrs={'placeholder':'Password','class':'form-control'}))
    new_password2 = forms.CharField(label="New password confirmation",
                                    widget=forms.PasswordInput(attrs={'placeholder':'Retype Password','class':'form-control'}))
class PasswordChangeForm(django_forms.PasswordChangeForm):
    new_password1 = forms.CharField(label="New password",
                                    widget=forms.PasswordInput(attrs={'placeholder':'Password','class':'form-control'}))
    new_password2 = forms.CharField(label="New password confirmation",
                                    widget=forms.PasswordInput(attrs={'placeholder':'Retype Password','class':'form-control'}))
    old_password = forms.CharField(label="Old password",
                                   widget=forms.PasswordInput(attrs={'placeholder':'Old Password','class':'form-control'}))

