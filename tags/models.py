from django.db import models
from thumbs.fields import ImageWithThumbsField
from django.conf import settings
import random

CODE_LENGTH = 8

class Tag(models.Model):
  name = models.CharField(max_length=64)
  code = models.CharField(blank=True, max_length=8)
  owner = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='tags')
  image = ImageWithThumbsField(upload_to='tag_images', sizes=((200,150),(300,250)))
  def __unicode__(self): return self.name
  def generate_code(self):
    return ''.join(random.choice('0123456789ABCDEFGHJKLMNPQRSTUVWXYZ') for i in range(CODE_LENGTH))
  def save(self, *args, **kwargs):
    while not self.code:
      code = self.generate_code()
      duplicates = Tag.objects.filter(code=code)
      if not duplicates: self.code = code
    super(Tag, self).save(*args, **kwargs)
