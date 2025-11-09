from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('about/', views.about, name='about'),
    path('contact/', views.contact, name='contact'),
    path('media/', views.media, name='media'),
    path('portfolio/', views.portfolio, name='portfolio'),
    path('graphicdesign/', views.graphicdesign, name='graphicdesign'),
    path('mobleapp/', views.mobileapp, name='mobileapp'),
    path('sham_about/', views.sham_about, name='sham_about'),
    path('smm/', views.smm, name='smm'),
    path('website/', views.website, name='website'),
    path('travel/', views.travel, name='travel'),
    path('decore/', views.decore, name='decore'),
    path('store/', views.store, name='store'),
    path('login/', views.login_user, name='login'),
    path('logout/', views.logout_user, name='logout'),
    path('signup/', views.signup_user, name ='signup'),
    path('accounts/login/', views.login_user, name='login'),
    path('update_user/', views.update_user, name ='update_user'),
    path('update_info/', views.update_info, name ='update_info'),
    path('update_password/', views.update_password, name ='update_password')
]