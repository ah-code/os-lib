import django.core
from django import forms
from django.contrib.auth.models import User
from django.db import models
from django.forms import ModelForm
from mptt.fields import TreeForeignKey
from mptt.models import MPTTModel
from django.core.urlresolvers import reverse
#from django.core.file.storage import FileSystemStorage

#fs = FileSystemStorage(location='/media/bookcover')

class Category(MPTTModel):
    name = models.CharField(max_length=64)
    slug = models.CharField(max_length=64)
    parent = TreeForeignKey('self', null=True, blank=True,
                            related_name='children')
    is_active = models.BooleanField()
    order = models.IntegerField()

    def __unicode__(self):
        return self.name

    class Meta:
        verbose_name_plural = "Categories"

    class MPTTMeta:
        order_insertion_by = ['order']

    def save(self, *args, **kwargs):
        super(Category, self).save(*args, **kwargs)
        Category.objects.rebuild()

class Author(models.Model):
    firstName = models.CharField(max_length=128)
    lastName = models.CharField(max_length=128)

    def __unicode__(self):
        return self.lastName

class Book(models.Model):
    title = models.CharField(max_length=128)
    author = models.ManyToManyField(Author)
    category = models.ForeignKey(Category)
    description = models.TextField()
    image = models.ImageField(upload_to='cover')
    #file
    file = models.FileField(upload_to='file')

    def	__unicode__(self):
        return self.title
#### NOT WORKING (why not????)	
	def get_absolute_url(self):
		#return reverse('book-details', self.id)
		return('details/'+ self.id)

class Lending(models.Model):
	user = models.ForeignKey(User)
	book = models.ForeignKey(Book)
	endDate = models.DateField()

class Favorite(models.Model):
    user = models.ForeignKey(User)
    book = models.ForeignKey(Book)
    endDate = models.DateField()