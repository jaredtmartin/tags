from authentication.models import User
from django.shortcuts import render_to_response, get_object_or_404
from django.http import HttpResponseRedirect, HttpResponse, Http404
from authentication.forms import UserForm, SimpleUserCreationFormWithFullName
from django.contrib.auth.tokens import default_token_generator
from django.core.urlresolvers import reverse
from django.template import RequestContext
from django.conf import settings
from django.utils.http import urlquote, base36_to_int
from django.contrib.sites.models import Site
from django.views.generic.edit import CreateView, UpdateView
from django.contrib.auth import forms as django_forms
from django.contrib import messages
# from vanilla import FormView
import vanilla
from django.views.decorators.csrf import csrf_protect

# # for LoginView
# from forms import LoginForm
# from django.utils.http import is_safe_url
# from django.contrib.auth import login as auth_login

class SignUp(vanilla.CreateView):
  model = User
  template_name = 'authentication/signup_form.html'
  email_template_name = 'authentication/signup_email.html'
  token_generator = default_token_generator
  form_class = SimpleUserCreationFormWithFullName
  def form_valid(self, form):
    opts = {}
    opts['use_https'] = self.request.is_secure()
    opts['token_generator'] = self.token_generator
    opts['email_template_name'] = self.email_template_name
    if not Site._meta.installed:
        opts['domain_override'] = RequestSite(request).domain
    form.save(**opts)
    messages.success(self.request, 'Congratulations! You account has been created successfully.')
    return HttpResponseRedirect(reverse('signup_done'))

class SignUpDone(vanilla.TemplateView):
  template_name = 'authentication/signup_done.html'

# def signup_done(request, template_name='registration/signup_done.html'):
#     return render_to_response(template_name, 
#                               context_instance=RequestContext(request))

class SignUpConfirm(vanilla.View):
  token_generator = default_token_generator
  def get(self, request, token, uidb36):
    assert uidb36 is not None and token is not None #checked par url
    try:
      uid_int = base36_to_int(uidb36)
    except ValueError:
      raise Http404
    user = get_object_or_404(User, id=uid_int)
    context = RequestContext(request)
    if self.token_generator.check_token(user, token):
      context['validlink'] = True
      user.is_active = True
      user.save()
    else:
      context['validlink'] = False
    return HttpResponseRedirect(reverse('signup_complete'))

# class LoginView(vanilla.FormView):
#   success_url = None
#   def get_form(self, data, files): return LoginForm(data)

#   def form_valid(self, form):
#     print 'request.POST.keys(): '+request.POST.keys()
#     # if not is_safe_url(url=request.POST['redirect_to'], host=request.get_host()):
#     #   redirect_to = resolve_url(settings.LOGIN_REDIRECT_URL)
#     return HttpResponseRedirect(self.get_success_url())

#   def form_invalid(self, form):
#     context = self.get_context_data(form=form)
#     return self.render_to_response(context)

#   def get_success_url(self):
#     if self.success_url is None:
#       msg = "'%s' must define 'success_url' or override 'form_valid()'"
#       raise ImproperlyConfigured(msg % self.__class__.__name__)
#     return self.success_url    


# def signup_confirm(request, uidb36=None, token=None,
#                    token_generator=default_token_generator,
#                    post_signup_redirect=None):
#     assert uidb36 is not None and token is not None #checked par url
#     if post_signup_redirect is None:
#         post_signup_redirect = reverse('signup_complete')
#     try:
#         uid_int = base36_to_int(uidb36)
#     except ValueError:
#         raise Http404

#     user = get_object_or_404(User, id=uid_int)
#     context_instance = RequestContext(request)

#     if token_generator.check_token(user, token):
#         context_instance['validlink'] = True
#         user.is_active = True
#         user.save()
#     else:
#         context_instance['validlink'] = False
#     return HttpResponseRedirect(post_signup_redirect)

class SignUpComplete(vanilla.TemplateView):
  template_name = 'authentication/signup_complete.html'
  
# def signup_complete(request, template_name='registration/signup_complete.html'):
#     return render_to_response(template_name, 
#                               context_instance=RequestContext(request, 
#                                                               {'login_url': settings.LOGIN_URL}))


class UserUpdateView(UpdateView):
  model=User
  form_class = UserForm
  # url = reverse('tags')
  def get_object(self, queryset=None):
        return self.request.user
  # def get_context_data(self, **kwargs):
  #   kwargs.update({
  #     'user_profile_form':UserProfileForm(instance=self.object.get_profile()),
  #   })
  #   return super(UserUpdateView, self).get_context_data(**kwargs)
  def form_invalid(self, form):
    return self.render_to_response(self.get_context_data(form=form))
  def form_valid(self, form):
    # user_profile_form.save()
    self.object = form.save()
    messages.success(self.request, 'The changes to your profile have been made successfully.')
    return self.render_to_response(self.get_context_data(form=form))
    # return super(UserUpdateView, self).form_valid(form)
  def post(self, request, *args, **kwargs):
    self.object = self.get_object()
    form_class = self.get_form_class()
    form = self.get_form(form_class)
    # user_profile_form = UserProfileForm(self.request.POST, instance=self.object.get_profile())
    if form.is_valid():
      print "form.cleaned_data:" + str(form.cleaned_data)
      return self.form_valid(form)
    else:
      return self.form_invalid(form)

# These imports are for LoginView
from django.views.decorators.csrf import csrf_protect
from django.views.decorators.cache import never_cache
from django.utils.decorators import method_decorator
from django.contrib.auth import REDIRECT_FIELD_NAME, login
from forms import LoginForm

class LoginView(vanilla.FormView):
  redirect_field_name = REDIRECT_FIELD_NAME
  template_name = 'authentication/login.html'
  form_class = django_forms.AuthenticationForm
  success_url = settings.LOGIN_REDIRECT_URL

  @method_decorator(csrf_protect)
  @method_decorator(never_cache)
  def dispatch(self, *args, **kwargs):
    return super(LoginView, self).dispatch(*args, **kwargs)

  def form_valid(self, form):
    """
    The user has provided valid credentials (this was checked in AuthenticationForm.is_valid()). So now we
    can check the test cookie stuff and log him in.
    """
    self.check_and_delete_test_cookie()
    user = form.get_user()
    login(self.request, user)
    # if user.force_change_password: return HttpResponseRedirect('/admin/password_change/')
    return super(LoginView, self).form_valid(form)

  def form_invalid(self, form):
    """
    The user has provided invalid credentials (this was checked in AuthenticationForm.is_valid()). So now we
    set the test cookie again and re-render the form with errors.
    """
    self.set_test_cookie()
    return super(LoginView, self).form_invalid(form)

  def get_success_url(self): return self.success_url

  def set_test_cookie(self):
    self.request.session.set_test_cookie()

  def check_and_delete_test_cookie(self):
    if self.request.session.test_cookie_worked():
      self.request.session.delete_test_cookie()
      return True
    return False

  def get(self, request, *args, **kwargs):
    """
    Same as django.views.generic.edit.ProcessFormView.get(), but adds test cookie stuff
    """
    self.set_test_cookie()
    return super(LoginView, self).get(request, *args, **kwargs)

class YesTagsLoginView(LoginView):
  def get_success_url(self): 
    if self.request.user.is_retailer: return reverse('list_clients')
    return self.success_url