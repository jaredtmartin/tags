from django.contrib import admin
from tags.models import Tag, Code, Event, Retailer


from django.utils.html import format_html
from django.core.urlresolvers import reverse

class LinkInline(admin.TabularInline):
	def get_link(self, url, instance): return format_html(u'<a href="{}">Edit: {}</a>', url, instance.name)
	def link(self, instance):
		# self.instance = instance
		url = reverse('admin:%s_%s_change' % (instance._meta.app_label, instance._meta.module_name), args=(instance.pk,))
		return self.get_link(url, instance)
	fields = ('link',)
	readonly_fields = ('link',)
	extra=0

class TagsInline(LinkInline):
  model = Tag
  def get_link(self, url, instance): return format_html(u'<a href="{}">{} {} {} {} {} {}</a>', url, instance.owner.first_name, instance.owner.last_name, instance.owner.email, instance.owner.phone, instance.code, instance.name)

class CodesInline(LinkInline):
  model = Code
  def get_link(self, url, instance): return format_html(u'<a href="{}">Edit: {}</a>', url, instance.code)

class TagAdmin(admin.ModelAdmin):
  list_display = ('name','code','image','owner')
def add_five_codes(modeladmin, request, queryset):
  for obj in queryset:
  	for i in range(5):
  		Code.objects.create(retailer=obj)
add_five_codes.short_description = "Add five codes to the selected retailer(s)"
def add_ten_codes(modeladmin, request, queryset):
  for obj in queryset:
  	for i in range(10):
  		Code.objects.create(retailer=obj)
add_ten_codes.short_description = "Add ten codes to the selected retailer(s)"
class RetailerAdmin(admin.ModelAdmin):
    actions = [add_five_codes, add_ten_codes]
    inlines = [
        TagsInline,
        CodesInline,
    ]

admin.site.register(Tag, TagAdmin)
admin.site.register(Code)
admin.site.register(Event)
admin.site.register(Retailer, RetailerAdmin)