from django import forms
from tags.models import Tag
class TagNameForm(forms.ModelForm):
  class Meta:
    model = Tag
    fields = ('name',)

class TagImageForm(forms.ModelForm):
  class Meta:
    model = Tag
    fields = ('image',)

class SearchForm(forms.Form):
  q = forms.CharField()

class ReportContactForm(forms.Form):
  name = forms.CharField()
  email = forms.CharField(required=False)
  phone = forms.CharField(required=False)
  def clean(self):
    cleaned_data = self.cleaned_data
    email=cleaned_data.get("email")
    phone = cleaned_data.get("phone")
    print "email = %s" % str(email)
    print "phone = %s" % str(phone)
    print "email and phone = %s" % str(email and phone)
    print "email or phone = %s" % str(email or phone)
    print "not email or phone = %s" % str(not email or phone)
    if not (email or phone):
      raise forms.ValidationError("You must enter at least one form of contact information for the owner to contact you.")
    # Always return the full collection of cleaned data.
    return cleaned_data

