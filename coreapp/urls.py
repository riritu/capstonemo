from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('unit/', views.unit, name='unit'),
    path('admins/', views.admins, name='admins'),
    path('creacc/', views.creacc, name='creacc'),
    path('ad_hom/', views.ad_hom, name='ad_hom'),
    path('ad_tent/', views.ad_tent, name='ad_tent'),
    path('tnt_hom/', views.tnt_hom, name='tnt_hom'),
    path('homepage/', views.homepage, name='homepage'),
    path('contact/', views.contact, name='contact'),
    path('vtour/', views.vtour, name='vtour'),
    path('amnts/', views.amnts, name='amnts'),
    path('book/', views.book, name='book'),
    path('comp/', views.comp, name='comp'),
    path('req/', views.req, name='req'),
    path('nav/', views.nav, name='nav'),
    path('pay/', views.pay, name='pay'),

]