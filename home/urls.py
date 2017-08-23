from django.conf.urls import url, include
from home import views
from home.views import HomeView

urlpatterns = [
    url(r'$', HomeView.as_view(), name='home'),
    url(r'^connect/(?P<operation>.+)/(?P<pk>\d+)/$', views.change_friends, name='change_friends')

]