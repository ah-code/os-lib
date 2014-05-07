from django.conf.urls import patterns, include, url
from django.contrib import admin
from django.contrib.auth import views as auth_views


admin.autodiscover()

from django.conf import settings
from booklib.views import PaginationView
from booklib import views

urlpatterns = patterns('',
    # Examples:
    url(r'^$', 'booklib.views.home', name='home'),
	url(r'^profile/$', 'booklib.views.profile', name='profile'),
    # url(r'^blog/', include('blog.urls')),
    url(r'^admin/', include(admin.site.urls)),
	(r'^demo/categories/$', 'booklib.views.show_categories'),
	(r'^demo/books/$', 'booklib.views.show_books'),
	url(r'^pagination$', PaginationView.as_view(), name='pagination'),

    url(r'^details$', views.details, name='views'),
 )

##Make sure it works on openshift as well at the moment
#if settings.DEBUG:
urlpatterns += patterns('',
    url(r'^media/(?P<path>.*)$', 'django.views.static.serve', {
        'document_root': settings.MEDIA_ROOT,
    }),
)

urlpatterns += patterns('',
#    url(r'', include('social_auth.urls')),
#	(r'^accounts/', include('registration.backends.default.urls')),
)

# Uncomment the next two lines to enable the admin:
from django.contrib import admin
admin.autodiscover()

urlpatterns += patterns('',

    # Uncomment the next line to enable the admin:
    url(r'^admin/', include(admin.site.urls)),
)

urlpatterns += patterns('django.contrib.auth.views',
#    url(r'^login/$', 'login', {'template_name': 'login.html'},
 #       name='mysite_login'),
#    url(r'^logout/$', 'logout', {'next_page': '/'}, name='mysite_logout'),
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
