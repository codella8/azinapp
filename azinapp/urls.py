from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('about/', views.about, name='about'),
    path('contact/', views.contact, name='contact'),
    path('services/', views.services, name='services'),
    path('portfolio/', views.portfolio, name='portfolio'),
    path('bussinessmanage/', views.bussinessmanage, name='bussinessmanage'),
    path('graphicdesign/', views.graphicdesign, name='graphicdesign'),
    path('marketing/', views.marketing, name='marketing'),
    path('mobleapp/', views.mobileapp, name='mobileapp'),
    path('sham_about/', views.sham_about, name='sham_about'),
    path('smm/', views.smm, name='smm'),
    path('website/', views.website, name='website'),
    path('travel/', views.travel, name='travel'),
    path('decore/', views.decore, name='decore'),
    path('store/', views.store, name='store'),
]