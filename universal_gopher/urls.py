from django.conf.urls import patterns, include, url
from universal_gopher import views

urlpatterns = patterns('universal_gopher.views',
    url(r'^$', 'index'),
    url(r'^home', 'index'),
    url(r'^films', 'films'),
    url(r'^film', 'film'),
    url(r'^coming_soon', 'coming_soon'),
    url(r'^about', 'about'),
    url(r'^login', 'index'),
    url(r'^logout', 'index'),
    url(r'^seating', 'seating'),
    url(r'^price', 'price'),
    url(r'^payment', 'payment'),
    url(r'^receipt', 'receipt'),
    url(r'^register', 'register'),
    url(r'^tickets', 'tickets')
   
)

handler404 = "universal_gopher.views.handler404"
