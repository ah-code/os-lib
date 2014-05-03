#from django.shortcuts import render_to_response
from django.shortcuts import render
from django.contrib.auth.views import login
from django.contrib.auth.decorators import login_required


def home(request):
    if (request.user.is_authenticated()):
        return render(request, 'home/home.html')
    return login(request, template_name='home/home.html')
