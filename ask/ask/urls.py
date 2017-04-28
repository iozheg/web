from django.conf.urls import include, url

from django.contrib import admin
from qa import views

admin.autodiscover()

urlpatterns = [
    # Examples:
    # url(r'^$', 'ask.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),

    url(r'^admin/', include(admin.site.urls)),
    url(r'login/', views.test),
    url(r'signup/', views.test),
    url(r'question/\d+/$', views.test),
    url(r'ask/', views.test),
    url(r'popular/', views.test),
    url(r'new/', views.test),
    url(r'^$', views.test),
]
