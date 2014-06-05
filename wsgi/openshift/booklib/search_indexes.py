import datetime
from haystack import indexes
from .models import Book
from .models import Author

#determines the index of search fields
#is used in templates-search-indexes-booklib-book_text.txt
class BookIndex(indexes.SearchIndex, indexes.Indexable):
	text = indexes.CharField(document=True, use_template=True)
	description = indexes.CharField(model_attr='description')
	title = indexes.CharField(model_attr='title')
	category = indexes.CharField(model_attr='category')
	author = indexes.CharField(model_attr='author', null=True)
    
	def get_model(self):
		return Book

	def prepare_authors(self, obj):
		return [author for author in obj.author.all()]
		
	def index_queryset(self, using=None):
        #Used when the entire index for model is updated."""
		return self.get_model().objects