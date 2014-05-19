from django.contrib import admin
from tags.models import Tag, Code, Event
class TagAdmin(admin.ModelAdmin):
    list_display = ('name','code','image','owner')
admin.site.register(Tag, TagAdmin)
admin.site.register(Code)
admin.site.register(Event)