import django.core
from django import forms
from django.contrib.auth.models import User
from django.db import models
from django.forms import ModelForm
from mptt.fields import TreeForeignKey
from mptt.models import MPTTModel
from django.core.urlresolvers import reverse
from mptt.managers import TreeManager
# signals for deleting files / images
from django.db.models.signals import pre_delete
from django.dispatch.dispatcher import receiver


class CategoryManager(TreeManager):
    pass

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
    category = TreeForeignKey(Category)
    description = models.TextField()
    image = models.ImageField(upload_to='cover')
    #file
    file = models.FileField(upload_to='file')

    def	__unicode__(self):
        return self.title
#### NOT WORKING (why not????)	
	#def get_absolute_url(self):
		#return reverse('book-details', self.id)
		#return('details/'+ self.id)

class Lending(models.Model):
	user = models.ForeignKey(User)
	book = models.ForeignKey(Book)
	endDate = models.DateField()

class Favorite(models.Model):
    user = models.ForeignKey(User)
    book = models.ForeignKey(Book)
    endDate = models.DateField()

#make sure that files and images are deleted if book is deleted	
@receiver(pre_delete, sender = Book)
def book_delete(sender, instance, **kwargs):
	#false so that the model is not saved again!
	instance.file.delete(false)
	instance.image.delete(false)