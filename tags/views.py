from vanilla import ListView, DetailView, UpdateView
from tags.models import Tag
from django.core.urlresolvers import reverse_lazy
from tags.forms import TagNameForm, TagImageForm
from django.contrib import messages

class AjaxUpdateView(UpdateView):
  success_message = None
  error_message = None
  def get_error_message(self, form):return self.error_message
  def get_success_message(self, form):return self.success_message
  def form_valid(self, form):
    # print "form Valid"
    # print "self.request.POST = %s" % str(self.request.POST)
    self.object = form.save()
    context = self.get_context_data(form=form)

    # Send message if appropriate
    msg=self.get_success_message(form)
    if msg: messages.success(self.request, msg)

    return self.render_to_response(context)

  def form_invalid(self, form):
    # print "Form Invalid"
    # print "form.errors = %s" % str(form.errors)
    # Send message if appropriate
    error_msg=self.get_error_message(form)
    if error_msg: messages.success(self.request, error_msg)
    return super(AjaxUpdateView, self).form_invalid(form)
#  For this project view and url names will follow verb_noun naming pattern.

class ListTags(ListView):
    model = Tag

class EditTag(UpdateView):
  model = Tag
  # We only use the GET, POST is done via AJAX
  def post(self, request, *args, **kwargs):
    return self.get(request, *args, **kwargs)

class TagNameAjax(AjaxUpdateView):
  model = Tag
  form_class = TagNameForm
  template_name = "tags/tag_name.html"
  error_message = "There was an error updating the tag's name."

class TagImageAjax(AjaxUpdateView):
  model = Tag
  form_class = TagImageForm
  template_name = "tags/tag_image.html"
  error_message = "There was an error updating the tag's image."
