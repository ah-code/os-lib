from django.contrib import admin
from .models import Author, Book, Category
from suit.admin import SortableModelAdmin
from mptt.admin import MPTTModelAdmin

#from django.db import models

# Register your models here.

#Classes for backend
#inherits from MPTT(Categories and enabled sorting (SortableModelAdmin))
class CategoryAdmin(MPTTModelAdmin, SortableModelAdmin):
	mptt_level_indent = 20
	search_fields = ('name', 'slug') 
	prepopulated_fields = {'slug': ('name',)}
	list_display = ('name', 'slug', 'is_active')
	list_editable = ('is_active',)
	list_display_links = ('name',)
	sortable = 'order'

#enables search, determines optics of backend
class AuthorAdmin(admin.ModelAdmin):
	search_fields = ('firstName', 'lastName')
	list_display = ('firstName', 'lastName')
	list_display_links = ('firstName', 'lastName')

class BookAdmin(admin.ModelAdmin):
	search_fields = ('title', 'description')
	list_display = ('title', 'category')

#registers the master data
admin.site.register(Author, AuthorAdmin)
admin.site.register(Book, BookAdmin)
admin.site.register(Category, CategoryAdmin)
