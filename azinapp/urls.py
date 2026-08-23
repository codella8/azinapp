from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('about/', views.about, name='about'),
    path('contact/', views.contact, name='contact'),
    
    # ======================================== #
    # AZIN MEDIA (Dropdown)                   #
    # ======================================== #
    path('media/', views.media, name='media'),
    path('graphicdesign/', views.graphicdesign, name='graphicdesign'),
    path('smm/', views.smm, name='smm'),
    
    # ======================================== #
    # AZIN GROUP (Dropdown)                   #
    # ======================================== #
    path('website/', views.website, name='website'),
    path('mobileapp/', views.mobileapp, name='mobileapp'),
    path('database/', views.database, name='database'),
    
    # ======================================== #
    # AZIN SHOP & DECORE                      #
    # ======================================== #
    path('shop/', views.shop, name='shop'),
    path('decore/', views.decore, name='decore'),
    
    # ======================================== #
    # EXTRA SERVICES                          #
    # ======================================== #
    path('store/', views.shop, name='store'),  # Redirect to shop
    
    # ======================================== #
    # AUTHENTICATION                          #
    # ======================================== #
    path('login/', views.login_user, name='login'),
    path('logout/', views.logout_user, name='logout'),
    path('signup/', views.signup_user, name='signup'),
    path('accounts/login/', views.login_user, name='login'),
    
    # ======================================== #
    # USER PROFILE                            #
    # ======================================== #
    path('profile/update/', views.update_user, name='update_user'),
    path('profile/info/', views.update_info, name='update_info'),
    path('profile/password/', views.update_password, name='update_password'),
]