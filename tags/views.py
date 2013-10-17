import vanilla
from tags.models import Tag
from django.core.urlresolvers import reverse
from django.http import HttpResponseRedirect
from tags.forms import TagNameForm, TagImageForm, SearchForm
from django.contrib import messages

class MessageMixin(object):
  success_message = None
  error_message = None
  def get_error_message(self, form):return self.error_message
  def get_success_message(self, form):return self.success_message
  def form_valid(self, form):
    msg=self.get_success_message(form)
    if msg: messages.success(self.request, msg)
    return super(MessageMixin, self).form_valid(form)

  def form_invalid(self, form):
    error_msg=self.get_error_message(form)
    if error_msg: messages.error(self.request, error_msg)
    return super(MessageMixin, self).form_invalid(form)
class UpdateView(MessageMixin, vanilla.UpdateView): pass
class FormView(MessageMixin, vanilla.FormView): pass

#  For this project view and url names will follow verb_noun naming pattern.

class ListTags(vanilla.ListView):
    model = Tag

class EditTag(vanilla.UpdateView):
  model = Tag
  # We only use the GET, POST is done via AJAX
  def post(self, request, *args, **kwargs):
    return self.get(request, *args, **kwargs)

class TagNameAjax(UpdateView):
  model = Tag
  form_class = TagNameForm
  template_name = "tags/tag_name.html"
  error_message = "There was an error updating the tag's name."

class TagImageAjax(UpdateView):
  model = Tag
  form_class = TagImageForm
  template_name = "tags/tag_image.html"
  error_message = "There was an error updating the tag's image."

class ShowTag(vanilla.DetailView):
  model = Tag

class SearchTag(FormView):
  form_class = SearchForm
  template_name="tags/search_form.html"
  def form_valid(self, form):
    results = Tag.objects.filter(code=form.cleaned_data['q'])
    if len(results)==1: 
      return HttpResponseRedirect(reverse("show_tag", kwargs={"pk":results[0].pk}))
    else: 
      messages.error(self.request, "We were unable to find the tag you were searching for. Please try again.")
      return self.form_invalid(form)

class ReportTag(vanilla.TemplateView):
  template_name="tags/report_contact_info.html"