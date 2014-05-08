from django.shortcuts import render
from django.shortcuts import render_to_response
from django.template import RequestContext
from .models import Category
from .models import Book
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.views.generic.base import TemplateView


# Create your views here.

from django.contrib.auth.views import login
from django.contrib.auth.decorators import login_required




def home(request):
    if (request.user.is_authenticated()):
		
        return render(request, 'home/home.html')
    return login(request, template_name='home/home.html')


@login_required
def profile(request):
    return render(request, template_name='home/profile.html')


def show_categories(request):
    return render_to_response("demo/categories.html",
                          {'nodes':Category.objects.all()},
                          context_instance=RequestContext(request))
						  

def show_books(request):
    book_list = Book.objects.all()
    paginator = Paginator(book_list, 5) # Show 5 books per page

    page = request.GET.get('page')
    try:
        books = paginator.page(page)
    except PageNotAnInteger:
        # If page is not an integer, deliver first page.
        books = paginator.page(1)
    except EmptyPage:
        # If page is out of range (e.g. 9999), deliver last page of results.
        books = paginator.page(paginator.num_pages)

    return render_to_response('demo/books.html', {"books": books}, context_instance=RequestContext(request))

class PaginationView(TemplateView):
    template_name = 'demo/pagination.html'

    def get_context_data(self, **kwargs):
        context = super(PaginationView, self).get_context_data(**kwargs)
		
        book_list = Book.objects.all()
        paginator = Paginator(book_list, 2)
        page = self.request.GET.get('page')
        try:
            show_lines = paginator.page(page)
        except PageNotAnInteger:
            # If page is not an integer, deliver first page.
            show_lines = paginator.page(1)
        except EmptyPage:
            # If page is out of range (e.g. 9999), deliver last page of results.
            show_lines = paginator.page(paginator.num_pages)
        context['lines'] = show_lines
        return context
		
	