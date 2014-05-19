from django import forms
from tags.models import Tag, Code
class TagNameForm(forms.ModelForm):
  class Meta:
    model = Tag
    fields = ('name',)

class TagImageForm(forms.ModelForm):
  class Meta:
    model = Tag
    fields = ('image',)
    
class TagRewardForm(forms.ModelForm):
  class Meta:
    model = Tag
    fields = ('reward',)
  reward = forms.CharField(required=False)

class SearchForm(forms.Form):
  q = forms.CharField()

class RegisterCodeForm(forms.Form):
  code = forms.CharField()
  def clean_code(self):
    data = self.cleaned_data['code']
    try: return Code.objects.get(code=self.cleaned_data['code'])
    except Code.DoesNotExist: raise forms.ValidationError("This is not a valid code.")
    return data

class ReportContactForm(forms.Form):
  name = forms.CharField()
  email = forms.CharField(required=False)
  phone = forms.CharField(required=False)
  def clean(self):
    cleaned_data = self.cleaned_data
    email=cleaned_data.get("email")
    phone = cleaned_data.get("phone")
    if not (email or phone):
      raise forms.ValidationError("You must enter at least one form of contact information for the owner to contact you.")
    # Always return the full collection of cleaned data.
    return cleaned_data

