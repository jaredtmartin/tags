from django.contrib import admin
from tags.models import Tag
class TagAdmin(admin.ModelAdmin):
    list_display = ('name','code','image','owner')
admin.site.register(Tag, TagAdmin)