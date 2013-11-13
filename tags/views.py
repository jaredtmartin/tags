import vanilla
from django.conf import settings
from tags.models import Tag
from django.core.urlresolvers import reverse
from django.http import HttpResponseRedirect
from tags.forms import TagNameForm, TagImageForm, SearchForm, ReportContactForm
from django.contrib import messages
from django.core.mail import send_mail
from django.contrib.sites.models import Site
from django.template import Context, loader
from django.utils.http import int_to_base36
from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import login_required

class LoginRequiredMixin(object):
  u"""Ensures that user must be authenticated in order to access view."""
  @method_decorator(login_required)
  def dispatch(self, *args, **kwargs):
    return super(LoginRequiredMixin, self).dispatch(*args, **kwargs)

class ExtraContextMixin(object):
  extra_context = {}
  def collect_bases(self, classType):
    bases = [classType]
    for baseClassType in classType.__bases__:
      bases += self.collect_bases(baseClassType)
    return bases
  def get_context_data(self, **kwargs):
    # Get the bases and remove duplicates
    bases = self.collect_bases(self.__class__)
    # for b in bases: print b
    bases.reverse()
    # print "======= Printing Bases ========"
    for base in bases:
      if hasattr(base, 'extra_context'):
        for key, value in base.extra_context.items():
          # print "key: %s value: %s" % (key, value)
          # First check to see if it's the name of a function
          if isinstance(value, basestring) and value[:4] == "get_": kwargs[key] = getattr(self,value)()
          # Otherwise, just add it to the context
          else: kwargs[key] = value
        # print "Base: %s Template: %s" % (base, kwargs.get('row_template_name',""))
        # for k,v in kwargs.items(): print "%s: %s" % (k,v)
    # print "==============================="
    # for key, value in kwargs.items(): print key+":"+str(value)
    return super(ExtraContextMixin, self).get_context_data(**kwargs)

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
    print "form.errors = %s" % str(form.errors)
    return super(MessageMixin, self).form_invalid(form)

class FilterMixin(object):
  filter_on = []
  def filter(self, queryset):
    # Takes a queryset and returns the queryset filtered
    # If you want to do a custom filter for a certain field,
    # Declare a function: filter_{{fieldname}} that takes a queryset and the value, 
    # does the filter and returns the queryset
    for f in self.filter_on:
      if hasattr(self,'filter_'+f): queryset = getattr(self,'filter_'+f)(queryset, self.request.GET.getlist(f,[]))
      elif f in self.request.GET: queryset = queryset.filter(**{f:self.request.GET[f]})
    return queryset
  def get_queryset(self):
    queryset = super(FilterMixin, self).get_queryset()
    if self.filter_on: queryset = self.filter(queryset)
    return queryset
  def get_context_data(self, **kwargs):
    context = super(FilterMixin, self).get_context_data(**kwargs)
    for filter_key in self.filter_on:
      if filter_key in self.request.GET: context[filter_key] = self.request.GET
    return context




class UpdateView(MessageMixin, vanilla.UpdateView): pass
class FormView(MessageMixin, vanilla.FormView): pass

#  For this project view and url names will follow verb_noun naming pattern.
class ListTags(FilterMixin, LoginRequiredMixin, vanilla.ListView):
  model = Tag
  filter_on=['owner']
  def filter_owner(self, qs, value):
    return qs.filter(owner=self.request.user)

class EditTag(LoginRequiredMixin, vanilla.UpdateView):
  model = Tag
  # We only use the GET, POST is done via AJAX
  def post(self, request, *args, **kwargs):
    return self.get(request, *args, **kwargs)

class TagNameAjax(LoginRequiredMixin, UpdateView):
  model = Tag
  form_class = TagNameForm
  template_name = "tags/tag_name.html"
  error_message = "There was an error updating the tag's name."

class TagImageAjax(LoginRequiredMixin, UpdateView):
  model = Tag
  form_class = TagImageForm
  template_name = "tags/tag_image.html"
  error_message = "There was an error updating the tag's image."

class ShowTag(vanilla.DetailView):
  model = Tag
  def get(self, request, *args, **kwargs):
    self.object = self.get_object()
    if self.request.user.is_authenticated and self.object.owner == self.request.user:
      return HttpResponseRedirect(reverse("edit_tag", kwargs={"pk":self.object.pk}))
    context = self.get_context_data()
    return self.render_to_response(context)

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

class EmailMixin(object):
  email_template_name = "email_template.html"
  def get_form(self, data=None, files=None, **kwargs):
    # Our form is not really a model form, so we'll drop the instance
    del kwargs['instance']
    return super(EmailMixin, self).get_form(data=data, files=files, **kwargs)
  def send_email(self, user, subject, domain_override=None, use_https=False, context={}):
    if not domain_override:
      current_site = Site.objects.get_current()
      site_name = current_site.name
      domain = current_site.domain
    else:
      site_name = domain = domain_override
    template = loader.get_template(self.email_template_name)
    context.update({
      'domain': domain,
      'site_name': site_name,
      'uid': int_to_base36(user.id),
      'user': user,
      'protocol': use_https and 'https' or 'http',
      })
    send_mail("Confirmation link sent on %s" % site_name,
              template.render(Context(context)), settings.EMAIL_HOST_USER, [user.email])

class ReportTag(EmailMixin, UpdateView):
  model = Tag
  template_name="tags/report_contact_form.html"
  form_class = ReportContactForm
  success_message = "Thank you! The owner will be informed immediately!"
  error_message='There was a problem sending your contact information to the owner.'
  email_template_name = "tags/report_email.html"
  def post(self, request, *args, **kwargs):
    self.object = self.get_object()
    if request.user.is_authenticated():
      self.send_email(self.object.owner, "Tag Located!", 
        context={
          'object':self.object,
          'name':request.user.get_full_name(),
          'email':request.user.email,
          'phone':request.user.phone
        }
      )
      messages.success(self.request, self.success_message)
      return HttpResponseRedirect(reverse("list_tags"))
    else:  
      form = self.get_form(data=request.POST, files=request.FILES, instance=self.object)
      if form.is_valid():
        return self.form_valid(form)
      return self.form_invalid(form)
  def form_valid(self, form):
    print "form.cleaned_data = %s" % str(form.cleaned_data)
    self.send_email(self.object.owner, "Tag Located!", 
      context={
        'object':self.object,
        'name':form.cleaned_data['name'],
        'email':form.cleaned_data['email'],
        'phone':form.cleaned_data['phone']
      }
    )
    messages.success(self.request, self.success_message)
    return HttpResponseRedirect(reverse("search"))