from django.shortcuts import render
from django.shortcuts import render_to_response
from django.template import RequestContext
from .models import Category
from .models import Book
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.views.generic.base import TemplateView
from django.shortcuts import get_object_or_404
from django.http import HttpResponse


# Create your views here.

from django.contrib.auth.views import login
from django.contrib.auth.decorators import login_required


def home(request):
    if (request.user.is_authenticated()):
		
        return render(request, 'home/home.html')
    return login(request, template_name='home/home.html')


@login_required
def profile(request):
	#@ Todo: Liste der Favoriten ausgeben, eventuell zu Buchseiten verlinken
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

    return render('demo/books.html', {"books": books}, context_instance=RequestContext(request))


def favorites(request, id):
	book = get_object_or_404(Book, pk=id)
	user = request.user
	
	#@ TODO: Favorite Object mit book und user machen, Uhrzeit hinterlegen, speichern
	return render_to_response('home/favorites.html', {"book":book}, context_instance=RequestContext(request))
	
def pdf_view(request, id):
	book =  get_object_or_404(Book, pk=id)
	pdf = book.file

	response = HttpResponse(pdf.read(), mimetype='application/pdf')
	response['Content-Disposition'] = 'inline;filename=some_file.pdf'
	return response
	pdf.closed

def details(request, id):
	book =  get_object_or_404(Book, pk=id)
	return render_to_response('demo/details.html', {"book":book}, context_instance=RequestContext(request))
	

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

    #http://stackoverflow.com/questions/10773144/how-to-send-url-parameter-in-post-request-without-form
    #in case of error, check link above
    def post_book(request):
        if request.method == 'POST':
            #try:
            book_list = Book.objects.all()
            #post the book title so we can get it in the detail view
            book_list.request.POST('title')
            #except KeyError:
                #pass

        return render_to_response('demo/details.html', {}, context_instance=RequestContext(request))


