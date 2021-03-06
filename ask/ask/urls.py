from django.conf.urls import include, url

from django.contrib import admin
from qa import views

admin.autodiscover()

urlpatterns = [
    # Examples:
    # url(r'^$', 'ask.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),

    url(r'^admin/', include(admin.site.urls)),
    #url(r'^/?page=\d+', views.new_questions),
    url(r'login/', views.login_view),
    url(r'logout/', views.logout_view),
    url(r'signup/', views.signup),
    url(r'question/(?P<question_id>\d+)/$', views.question_details),
    url(r'ask/', views.ask_form),
    url(r'popular/', views.popular_questions),
    #url(r'new/', views.test),
    url(r'^$', views.new_questions),
]
