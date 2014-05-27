from django.db import models
from thumbs.fields import ImageWithThumbsField
from django.conf import settings
from authentication.models import User
import random

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

class Client(models.Model):
  retailer = models.ForeignKey(Retailer, related_name='clients')
  user = models.OneToOneField(User)
  created_at = models.DateTimeField(auto_now_add=True)