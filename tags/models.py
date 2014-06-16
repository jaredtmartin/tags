from django.db import models
from thumbs.fields import ImageWithThumbsField
from django.conf import settings
from authentication.models import User
import random
from django.template import Context, loader
from django.core.mail import send_mail

CODE_LENGTH = 8

class Retailer(models.Model):
  name = models.CharField(max_length=64)
  email = models.CharField(max_length=64)
  user = models.OneToOneField(User)
  def __unicode__(self): return self.name

class Tag(models.Model):
  name = models.CharField(max_length=64)
  code = models.CharField(blank=False, max_length=8)
  retailer = models.ForeignKey(Retailer, related_name='tags')
  owner = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='tags')
  image = ImageWithThumbsField(upload_to='tag_images', sizes=((200,150),(300,250)))
  reward = models.CharField(max_length=128)
  def __unicode__(self): return self.name
  
class Code(models.Model):
  retailer = models.ForeignKey(Retailer, related_name='codes')
  code = models.CharField(blank=True, max_length=8)
  def generate_code(self):
    return ''.join(random.choice('0123456789ABCDEFGHJKLMNPQRSTUVWXYZ') for i in range(CODE_LENGTH))
  def save(self, *args, **kwargs):
    while not self.code:
      code = self.generate_code()
      if Tag.objects.filter(code=code): code = None
      if Code.objects.filter(code=code): code = None
      if code: self.code = code
    super(Code, self).save(*args, **kwargs)
  def __unicode__(self): return self.code

class Event(models.Model):
  tag = models.ForeignKey(Tag, related_name='events')
  owner = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='events')
  details = models.CharField(max_length=64)
  tipo = models.CharField(max_length=16)
  created_at = models.DateTimeField(auto_now_add=True)
  viewed = models.BooleanField(default=False)
  name = models.CharField(max_length=64)
  email = models.CharField(max_length=64)
  phone = models.CharField(max_length=64)
  reward = models.CharField(max_length=64)
  def __unicode__(self): return self.tag.name + ' ' + self.tipo
  def send_notifications(self):
    if self.tag.owner.email: self.send_email_notification()
    if self.tag.owner.phone: self.send_sms_notification()
  def send_email_notification(self):
    template = loader.get_template('tags/tag_found_email.html')
    admin_template = loader.get_template('tags/tag_found_admin_email.html')
    context = Context({
      'tag':self.tag,
      'name':self.name,
      'email':self.email,
      'phone':self.phone,
      'reward':self.reward,
    })
    send_mail("YesTag Located!", template.render(context), settings.EMAIL_HOST_USER, [self.tag.owner.email])
    send_mail("YesTag Located!", admin_template.render(context), settings.EMAIL_HOST_USER, [self.tag.owner.email])
  def send_sms_notification(self):
    import urllib2
    import urllib
    template = loader.get_template('tags/tag_found_sms.html')
    context = Context({
      'tag':self.tag,
      'name':self.name,
      'email':self.email,
      'phone':self.phone,
    })
    data = {
      'uid':'4d616a65656d', 
      'pin':'538d54bf7c684',
      'route':5,
      'mobile':self.tag.owner.phone,
      'message':template.render(context),
      'sender'='YESTAG',
      'pushid'=1,
      'tempid'=16110,
    }
    url_values = urllib.urlencode(data)
    url = 'http://smsapp.ideations4.com/api/sms.php'
    full_url = url + '?' + url_values
    data = urllib2.urlopen(full_url)

class Client(models.Model):
  retailer = models.ForeignKey(Retailer, related_name='clients')
  user = models.OneToOneField(User)
  created_at = models.DateTimeField(auto_now_add=True)