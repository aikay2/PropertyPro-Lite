from django.contrib import admin
from .models import Property, PropertyImage, Flags

# Register your models here.

class PropertyAdmin(admin.ModelAdmin):
    list_display = ('type', 'city', 'status', 'price', 'created_on')
    list_filter = ('type', 'city', 'status')
    search_fields = ('address',)


admin.site.register(Property, PropertyAdmin)
admin.site.register(PropertyImage)
admin.site.register(Flags)
