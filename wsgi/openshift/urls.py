from django.conf.urls import patterns, include, url
from django.contrib import admin
from django.contrib.auth import views as auth_views
from django.conf import settings
from booklib.views import PaginationView
from booklib import views
import haystack
from haystack.forms import SearchForm
from haystack.query import SearchQuerySet
from haystack.views import SearchView

# Uncomment the next two lines to enable the admin:
from django.contrib import admin
admin.autodiscover()

#main URLs
urlpatterns = patterns('',
    url(r'^$', 'booklib.views.home', name='home'),
	url(r'^profile/$', 'booklib.views.profile', name='profile'),
    url(r'^admin/', include(admin.site.urls)),
    url(r'^about', 'booklib.views.about', name = 'about'),
	url(r'^browse$', PaginationView.as_view(), name='pagination'),
    url(r'^pagination/details$', views.details, name='details'),
	url(r'^details/(?P<id>[0-9]+)/$', views.details, name = 'book-details'),
	url(r'^favorites/(?P<id>[0-9]+)/$', views.favorites, name = 'book-favorites'),
	url(r'^book_pdf/(?P<id>[0-9]+)/$', views.pdf_view, name = 'book-pdf'),
)

#search URLs
urlpatterns += patterns('haystack.views',
    url(r'search/', SearchView(
        template='search/search.html',
        form_class=SearchForm
    ), name='haystack_search'),
)

#media URLs for openshift
##Make sure it works on openshift as well at the moment
#if settings.DEBUG:
urlpatterns += patterns('',
    url(r'^media/(?P<path>.*)$', 'django.views.static.serve', {
        'document_root': settings.MEDIA_ROOT,
    }),
)

#registration URLs
urlpatterns += patterns('django.contrib.auth.views',
    url(r'^login/$', 'login', {'template_name': 'login.html'},
        name='mysite_login'),
    url(r'^logout/$', 'logout', {'next_page': '/'}, name='mysite_logout'),
	url(r'^accounts/', include('registration.backends.default.urls')),
	url(r'^password/change/$',
                    auth_views.password_change,
                    name='password_change'),
    url(r'^password/change/done/$',
                    auth_views.password_change_done,
                    name='password_change_done'),
    url(r'^password/reset/$',
                    auth_views.password_reset,
                    name='password_reset'),
    url(r'^accounts/password/reset/done/$',
                    auth_views.password_reset_done,
                    name='password_reset_done'),
    url(r'^password/reset/complete/$',
                    auth_views.password_reset_complete,
                    name='password_reset_complete'),
    url(r'^password/reset/confirm/(?P<uidb64>[0-9A-Za-z_\-]+)/(?P<token>.+)/$',
                    auth_views.password_reset_confirm,
                    name='password_reset_confirm'),

)
