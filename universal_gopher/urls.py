# from django.conf.urls import patterns, include, url
from django.conf.urls import url, include
from universal_gopher import views

# urlpatterns = patterns('universal_gopher.views',
urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'^home', views.index, name='index'),
    url(r'^films', views.films, name='films'),
    url(r'^film', views.film, name='film'),
    url(r'^coming_soon', views.coming_soon, name='coming_soon'),
    url(r'^about', views.about, name='about'),
    url(r'^login', views.login, name='index'),
    url(r'^logout', views.logout, name='index'),
    url(r'^seating', views.seating, name='seating'),
    url(r'^price', views.price, name='price'),
    url(r'^payment', views.payment, name='payment'),
    url(r'^receipt', views.receipt, name='receipt'),
    url(r'^register', views.register, name='register'),
    url(r'^tickets', views.tickets, name='tickets')
   
]

# handler404 = "universal_gopher.views.handler404"
