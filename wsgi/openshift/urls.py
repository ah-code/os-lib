from django.conf.urls import patterns, include, url
from django.contrib import admin

admin.autodiscover()

from django.conf import settings
from booklib.views import PaginationView

urlpatterns = patterns('',
    # Examples:
    url(r'^$', 'views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),
    url(r'^admin/', include(admin.site.urls)),
	(r'^demo/categories/$', 'booklib.views.show_categories'),
	(r'^demo/books/$', 'booklib.views.show_books'),
	url(r'^pagination$', PaginationView.as_view(), name='pagination'),
)

##Make sure it works on openshift as well at the moment
#if settings.DEBUG:
urlpatterns += patterns('',
    url(r'^media/(?P<path>.*)$', 'django.views.static.serve', {
        'document_root': settings.MEDIA_ROOT,
    }),
)
urlpatterns += patterns('',
    url(r'', include('social_auth.urls')),
)

# Uncomment the next two lines to enable the admin:
from django.contrib import admin
admin.autodiscover()

urlpatterns += patterns('',
    # Uncomment the next line to enable the admin:
    url(r'^admin/', include(admin.site.urls)),

)

urlpatterns += patterns('django.contrib.auth.views',
    url(r'^login/$', 'login', {'template_name': 'login.html'},
        name='mysite_login'),
    url(r'^logout/$', 'logout', {'next_page': '/'}, name='mysite_logout'),
)
