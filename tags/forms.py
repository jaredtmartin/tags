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