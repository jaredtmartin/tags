from django.http import HttpResponseRedirect

import re

class PasswordChangeMiddleware:
  def process_request(self, request):
  	if request.user.is_authenticated() and \
    	request.user.force_change_password and \
      not re.match(r'^/auth/password_change/', request.path):
				return HttpResponseRedirect('/auth/password_change/')