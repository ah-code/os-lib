from django.contrib import admin
from .models import Author, Book, Category
from suit.admin import SortableModelAdmin
#from django.db import models

# Register your models here.

class CategoryAdmin(MPTTModelAdmin), SortableModelAdmin:
	mptt_level_indent = 20
	search_fields = ('name', 'slug') 
	prepopulated_fields = {'slug': ('name',)}
	list_display = ('name', 'slug', 'is_active')
	list_editable = ('is_active')
	list_display_links = ('name',)
	sortable = 'order'


admin.site.register(Author)
admin.site.register(Book)
admin.site.register(Category, CategoryAdmin)
