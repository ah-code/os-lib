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


# Create your views here.

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

    #@ Todo: Liste der Favoriten ausgeben, eventuell zu Buchseiten verlinken
    favs = Favorite.objects.filter(user_id=request.user.id)
    paginator = Paginator(favs, 5)


    page = request.GET.get('page')

    try:
		favs = paginator.page(page)
    except PageNotAnInteger:
     # If page is not an integer, deliver first page.
        favs = paginator.page(1)
    except EmptyPage:
            # If page is out of range (e.g. 9999), deliver last page of results.
        favs = paginator.page(paginator.num_pages)

    #return render(request,{'favorites':favs}, template_name='home/profile.html')
    return render_to_response('home/profile.html', {"favorites": favs}, context_instance=RequestContext(request))


						  

@login_required
def favorites(request, id):
    book = get_object_or_404(Book, pk=id)
    user = request.user

    try:
        fav = Favorite.objects.get(book = book, user = user)
        fav.delete()
        message = "deleted"
    except Favorite.DoesNotExist:
        fav = Favorite()
        fav.book = book
        fav.user = user
        fav.endDate = datetime.date.today()
        fav.save()
        message = "created"


    #@ TODO: Favorite Object mit book und user machen, Uhrzeit hinterlegen, speichern
    return render_to_response('home/favorites.html', {"book":book, 'message':message}, context_instance=RequestContext(request))
@login_required	
def pdf_view(request, id):
	if (request.user.is_authenticated()):
		book =  get_object_or_404(Book, pk=id)
		pdf = book.file
		
		today = datetime.date.today()
		lend = Lending (user = request.user, book = book, endDate = today)
		lend.save()
		response = HttpResponse(pdf.read(), mimetype='application/pdf')
		response['Content-Disposition'] = 'inline;filename=some_file.pdf'
		return response
		pdf.closed
	return login(request, template_name='registration/login.html')
	
@login_required
def details(request, id):
	if (request.user.is_authenticated()):
		book =  get_object_or_404(Book, pk=id)
		today = datetime.date.today()
		lending = Lending.objects.filter(user = request.user, endDate__month = today.month)
		c = lending.count()
		c = 10-c
		fav = Favorite.objects.filter(user = request.user, book = book)
		f = fav.count()
	
		return render_to_response('main/details.html', {"book":book, "lendings": c, "favorite":f}, context_instance=RequestContext(request))
	return login(request, template_name='registration/login.html')

class PaginationView(TemplateView):
    template_name = 'main/pagination.html'

    def get_context_data(self, **kwargs):
        context = super(PaginationView, self).get_context_data(**kwargs)
        context['lines'] = Book.objects.all().order_by('category')
        return context



