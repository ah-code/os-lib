from django.contrib import admin
from django.contrib.admin import ModelAdmin, SimpleListFilter

from mptt.admin import MPTTModelAdmin
from category.models import Category

class CategoryAdmin(MPTTModelAdmin):
    mptt_level_indent = 20
    search_fields = ('name', 'slug')
    prepopulated_fields = {'slug': ('name',)}
    list_display = ('name', 'slug', 'is_active')
    list_editable = ('is_active',)
    list_display_links = ('name',)
    sortable = 'order'
	
admin.site.register(Category, CategoryAdmin)