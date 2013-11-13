from django.db import models
from thumbs.fields import ImageWithThumbsField
from django.conf import settings
import random

CODE_LENGTH = 8

class Tag(models.Model):
  name = models.CharField(max_length=64)
  code = models.CharField(blank=False, max_length=8)
  owner = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='tags')
  image = ImageWithThumbsField(upload_to='tag_images', sizes=((200,150),(300,250)))
  def __unicode__(self): return self.name

class Report(models.Model):
  tag = models.ForeignKey(Tag) 
  name = models.CharField(max_length=64)
  email = models.CharField(max_length=64)
  phone = models.CharField(max_length=64)

class Code(models.Model):
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
