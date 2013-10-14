from django.db import models
from django.contrib.auth.models import User
from thumbs.fields import ImageWithThumbsField

class Tag(models.Model):
    name = models.CharField(max_length=64)
    owner = models.ForeignKey(User, related_name='tags')
    image = ImageWithThumbsField(upload_to='tag_images', sizes=((200,150),(300,250)))
    def __unicode__(self): return self.name
