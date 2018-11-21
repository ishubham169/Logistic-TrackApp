from django.conf.urls import url
from . import views
#from django.contrib.auth.views import login

urlpatterns=[
url(r'^$',views.home),
url(r'^get_details/$',views.track_it),

]