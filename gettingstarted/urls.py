from django.conf.urls import include, url
from django.urls import path

# from django.contrib import admin
# admin.autodiscover()

import train_times.views

# Examples:
# url(r'^$', 'gettingstarted.views.home', name='home'),
# url(r'^blog/', include('blog.urls')),

urlpatterns = [
    path('', train_times.views.index, name='index'),
    path('<stop_id>/', train_times.views.one_stop_with_id, name='one_stop_with_id'),
]
# urlpatterns = [
#     url(r'^$', train_times.views.index, name='index'),
#     url(r'^db', train_times.views.db, name='db'),
#     path('admin/', admin.site.urls),
# ]
