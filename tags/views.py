import vanilla
from django.conf import settings
from tags.models import Tag, Event, Client
from authentication.models import User
from django.core.urlresolvers import reverse
from django.http import HttpResponseRedirect
from tags.forms import TagNameForm, TagImageForm, SearchForm, ReportContactForm, RegisterCodeForm, \
  TagRewardForm, SMSFoundForm
from django.contrib import messages
from django.core.mail import send_mail
from django.contrib.sites.models import Site
from django.template import Context, loader
from django.utils.http import int_to_base36
from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import login_required
from django.views.generic import View
from django.core.urlresolvers import reverse_lazy

def get_found_message(name, phone, email=''):
  msg='by: '+name
  if phone: msg += ' '+phone
  if email: msg += ' '+email
  return msg
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

  def get_context_data(self, **kwargs):
    context = super(MessageMixin, self).get_context_data(**kwargs)
    print ("self.request.user.is_authenticated():"+str(self.request.user.is_authenticated()))
    if self.request.user.is_authenticated(): 
      context['found_events'] = Event.objects.filter(viewed=False, tipo='Found', owner=self.request.user)
    return context
  def form_invalid(self, form):
    error_msg=self.get_error_message(form)
    if error_msg: messages.error(self.request, error_msg)
    print "form.errors = %s" % str(form.errors)
    return super(MessageMixin, self).form_invalid(form)

class ReportMessagesMixin(object):
  pass
  # def get_context_data(self, **kwargs):
  #   context = super(ReportMessagesMixin, self).get_context_data(**kwargs)
  #   if self.request.user.is_authenticated():
  #     for event in Event.objects.filter(viewed=False, tipo='Found', owner=self.request.user):
  #       msg = 'Your item, %s has been found! <a href="%s">Click here to get it back.</a>' % (event.tag.name,'')
  #       messages.success(self.request, msg)
  #   return context

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
class ListTags(FilterMixin, MessageMixin, LoginRequiredMixin, vanilla.ListView):
  model = Tag
  filter_on=['owner']
  def filter_owner(self, qs, value):
    return qs.filter(owner=self.request.user)

class EditTag(MessageMixin, LoginRequiredMixin, vanilla.UpdateView):
  model = Tag
  # We only use the GET, POST is done via AJAX
  def post(self, request, *args, **kwargs):
    return self.get(request, *args, **kwargs)

class AjaxUpdateView(UpdateView):
  def form_valid(self, form):
    self.object = form.save()
    context = self.get_context_data(form=form)
    # Send message if appropriate
    msg=self.get_success_message(form)
    if msg: messages.success(self.request, msg)
    return self.render_to_response(context)

  def form_invalid(self, form):
    # Send message if appropriate
    error_msg=self.get_error_message(form)
    if error_msg: messages.success(self.request, error_msg)
    return super(AjaxUpdateView, self).form_invalid(form)
#  For this project view and url names will follow verb_noun naming pattern.

class AjaxEventView(AjaxUpdateView):
  def form_valid(self, form):
    self.object = form.save()
    event = self.create_event(self.object)
    context = self.get_context_data(form=form, event=event)
    # Send message if appropriate
    msg=self.get_success_message(form)
    if msg: messages.success(self.request, msg)
    return self.render_to_response(context)

class TagNameAjax(AjaxEventView):
  model = Tag
  form_class = TagNameForm
  template_name = "tags/tag_name.html"
  error_message = "There was an error updating the tag's name."
  def create_event(self, object):
    return Event.objects.create(tag=object, tipo='Name Changed', details="to: " + object.name, owner = object.owner)

class TagRewardAjax(AjaxEventView):
  model = Tag
  form_class = TagRewardForm
  template_name = "tags/tag_reward.html"
  error_message = "There was an error updating the tag's reward."

  def create_event(self, object):
    return Event.objects.create(tag=object, tipo='Reward Changed', details="to: " + object.reward, owner = object.owner)

class TagImageAjax(AjaxEventView):
  model = Tag
  form_class = TagImageForm
  template_name = "tags/tag_image.html"
  error_message = "There was an error updating the tag's image."
  def create_event(self, object): 
    return Event.objects.create(tag=object, tipo='Image Changed', details="", owner = object.owner)

class ShowTag(vanilla.DetailView, ReportMessagesMixin):
  model = Tag
  def get(self, request, *args, **kwargs):
    self.object = self.get_object()
    if self.request.user.is_authenticated and self.object.owner == self.request.user:
      return HttpResponseRedirect(reverse("edit_tag", kwargs={"pk":self.object.pk}))
    context = self.get_context_data()
    return self.render_to_response(context)

class SearchTag(FormView, ReportMessagesMixin):
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
    if 'instance' in kwargs: del kwargs['instance']
    return super(EmailMixin, self).get_form(data=data, files=files, **kwargs)
  def send_email(self, user, subject, domain_override=None, use_https=False, context={}, template=None):
    if not domain_override:
      current_site = Site.objects.get_current()
      site_name = current_site.name
      domain = current_site.domain
    else:
      site_name = domain = domain_override
    if not subject: subject = "Confirmation link sent on %s" % site_name
    if not template: template = loader.get_template(self.email_template_name)
    context.update({
      'domain': domain,
      'site_name': site_name,
      'uid': int_to_base36(user.id),
      'user': user,
      'protocol': use_https and 'https' or 'http',
      })
    send_mail(subject, template.render(Context(context)), settings.EMAIL_HOST_USER, [user.email])

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
    msg = get_found_message(form.cleaned_data['name'], form.cleaned_data['phone'], form.cleaned_data['email'])
    Event.objects.create(
      tag = self.object, 
      tipo = 'Found', 
      details = msg, 
      name = form.cleaned_data['name'],
      email = form.cleaned_data['email'],
      phone = form.cleaned_data['phone'],
      owner = self.object.owner,
      reward = self.object.reward
    )
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

class RegisterTag(FormView):
  form_class = RegisterCodeForm
  template_name = "tags/tag_register_form.html"
  success_message = "Your new tag has been registered successfully."
  def form_valid(self, form):
    code = form.cleaned_data['code']
    tag = Tag.objects.create(owner=self.request.user, code=code, name="New Tag", retailer=code.retailer)
    Event.objects.create(tag=tag, tipo='Registered', details="", owner = tag.owner)
    client, created = Client.objects.get_or_create(user=self.request.user, retailer = tag.retailer)
    code.delete()
    messages.success(self.request, self.success_message)
    return HttpResponseRedirect(reverse('edit_tag', kwargs={'pk':tag.pk}))

class HowItWorks(MessageMixin, vanilla.TemplateView):
  template_name = 'tags/how_it_works.html'
  
class Home(MessageMixin, vanilla.TemplateView):
  template_name = 'tags/landing.html'

class ViewEvent(vanilla.DetailView):
  model = Event

class DismissEvent(vanilla.UpdateView):
  model = Event
  template_name = "design/ajax.html"
  def post(self, request, *args, **kwargs):
    self.object = self.get_object()
    self.object.viewed = True
    self.object.save()
    return self.render_to_response({})

class ListClients(FilterMixin, MessageMixin, LoginRequiredMixin, vanilla.ListView):
  model = Client
  filter_on=['retailer']
  def filter_retailer(self, qs, value):
    return qs.filter(retailer__user = self.request.user)

class SMSFound(vanilla.FormView):
  model = Tag
  form_class = SMSFoundForm
  template_name = 'tags/SMSFoundForm.html'
  email_template_name = "tags/report_email.html"
  success_url = reverse_lazy('list_tags')
  def post(self, request):
    self.data = request.POST
    return self.process_form()
  def get(self, request, *args, **kwargs):
    self.data = request.GET
    return self.process_form()
  def process_form(self):
    form = self.get_form(data=self.data)
    if form.is_valid(): return self.form_valid(form)
    return self.form_invalid(form)
  def form_valid(self, form):
    self.object = form.cleaned_data['tag']
    msg = get_found_message('Someone', form.cleaned_data['number'])
    Event.objects.create(
      tag = self.object,
      tipo = 'Found', 
      details = msg, 
      name = 'Someone',
      email = '',
      phone = form.cleaned_data['number'],
      owner = self.object.owner,
      reward = self.object.reward
    )
    template = loader.get_template('tags/SMSFoundEmail.html')
    send_mail("Tag Located!", 
      template.render(Context({
        'object':self.object,
        'phone':form.cleaned_data['number']
      })), settings.EMAIL_HOST_USER, [self.object.owner.email])

    return HttpResponseRedirect(self.get_success_url())
  def form_invalid(self, form):
    template = loader.get_template('tags/SMSIncomplete.html')
    send_mail("Incomplete SMS recieved", 
      template.render(Context({
        'message':self.data['tag'],
        'number':self.data['number']
      })), settings.EMAIL_HOST_USER, ['jaredtmartin@gmail.com'])
    context = self.get_context_data(form=form)
    return self.render_to_response(context)