from django.shortcuts import render
from django.shortcuts import render_to_response
from django.template import RequestContext
from .models import Category
from .models import Book, Favorite, Lending
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.views.generic.base import TemplateView
from django.shortcuts import get_object_or_404
from django.http import HttpResponse
import datetime
from django.contrib.auth.views import login
from django.contrib.auth.decorators import login_required


def home(request):
    if (request.user.is_authenticated()):
        return render(request, 'home/home.html')
    return login(request, template_name='home/home.html')

def about(request):
    return render(request, 'home/about.html')

@login_required
def profile(request):
    favs = Favorite.objects.filter(user_id=request.user.id)
    #second page is created if number of favorites is >5
    paginator = Paginator(favs, 5)
    #selection is committed e.g. page 2
    page = request.GET.get('page')

    try:
        #display favorites of selected page e.g. favorites from page 2
		favs = paginator.page(page)
    except PageNotAnInteger:
        # If page is not an integer, deliver first page.
        favs = paginator.page(1)
    except EmptyPage:
        # If page is out of range (e.g. 9999), deliver last page of results.
        favs = paginator.page(paginator.num_pages)

    return render_to_response('home/profile.html', {"favorites": favs}, context_instance=RequestContext(request))

@login_required
def favorites(request, id):
    book = get_object_or_404(Book, pk=id)
    user = request.user

    try:
        #if this book is already a favorite -> delete the favorite
        fav = Favorite.objects.get(book = book, user = user)
        fav.delete()
        message = "deleted"
    except Favorite.DoesNotExist:
        #add book to favorites (inc. user and date)
        fav = Favorite()
        fav.book = book
        fav.user = user
        fav.endDate = datetime.date.today()
        fav.save()
        message = "created"

    return render_to_response('home/favorites.html', {"book":book, 'message':message}, context_instance=RequestContext(request))

@login_required
def pdf_view(request, id):
    #pass the book-id to get the pdf file and save the current date
    book =  get_object_or_404(Book, pk=id)
    pdf = book.file
    today = datetime.date.today()
    lend = Lending (user = request.user, book = book, endDate = today)
    lend.save()
    response = HttpResponse(pdf.read(), mimetype='application/pdf')
    response['Content-Disposition'] = 'inline;filename=some_file.pdf'
    return response
    pdf.closed

@login_required
def details(request, id):
		book =  get_object_or_404(Book, pk=id)
		today = datetime.date.today()
		lending = Lending.objects.filter(user = request.user, endDate__month = today.month)
        #count how many books have been downloaded
		c = lending.count()
		c = 10-c
		fav = Favorite.objects.filter(user = request.user, book = book)
		f = fav.count()
		return render_to_response('main/details.html', {"book":book, "lendings": c, "favorite":f}, context_instance=RequestContext(request))

#alternative (more modern) way to do view classes
class PaginationView(TemplateView):
    template_name = 'main/browsing.html'

    #group books by category to display the category menu in the browse page
    def get_context_data(self, **kwargs):
        context = super(PaginationView, self).get_context_data(**kwargs)
        context['lines'] = Book.objects.all().order_by('category')
        return context



