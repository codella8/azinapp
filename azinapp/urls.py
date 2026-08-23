from django.urls import path
from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from . import views

urlpatterns = [
    path('admin-panel/', views.admin_panel, name='admin_panel'),
    
    # ======================================== #
    # MAIN PAGES                              #
    # ======================================== #
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

# ======================================== #
# STATIC & MEDIA FILES (Development)       #
# ======================================== #

if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)