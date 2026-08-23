from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import user_passes_test, login_required
from django.contrib.auth.models import User
from django.core.mail import send_mail
from django.conf import settings
from django.utils.translation import gettext as _
from django.utils.text import slugify

from .models import (
    Team, Profile, Contact,
    MediaGallery,
    GraphicDesignProject,
    SMMProject,
    WebProject,
    MobileAppProject,
    DatabaseProject,
    ShopProduct,
    DecoreProject,
)
from .forms import (
    ContactForm, SignUpForm, UserUpdateForm, 
    UpdatePasswordForm, UpdateUserInfo
)


# ======================================== #
# 1. ADMIN PANEL                          #
# ======================================== #

def admin_only(user):
    return user.is_staff

@user_passes_test(admin_only)
def admin_panel(request):
    return redirect('admin:index')


# ======================================== #
# 2. TEST VIEW                            #
# ======================================== #

def my_view(request):
    output = _("Welcome to AZIN GROUP.")
    return HttpResponse(output)


# ======================================== #
# 3. HOME PAGE                            #
# ======================================== #

def index(request):
    featured_media = MediaGallery.objects.filter(is_featured=True, is_published=True)[:6]
    
    context = {
        'featured_media': featured_media,
    }
    return render(request, 'index.html', context)


# ======================================== #
# 4. ABOUT PAGE                           #
# ======================================== #

def about(request):
    team = Team.objects.all()
    return render(request, "about.html", {"team": team})


# ======================================== #
# 5. CONTACT PAGE                         #
# ======================================== #

def contact(request):
    if request.method == "POST":
        form = ContactForm(request.POST)
        if form.is_valid():
            contact = form.save()
            
            # Send email notification
            try:
                send_mail(
                    subject=f"New Message from {contact.name}",
                    message=f"From: {contact.name} <{contact.email}>\n\n{contact.message}",
                    from_email=settings.DEFAULT_FROM_EMAIL,
                    recipient_list=[settings.DEFAULT_FROM_EMAIL],
                    fail_silently=True,
                )
            except:
                pass
            
            messages.success(request, _("Your message has been sent successfully!"))
            return redirect("contact")
    else:
        form = ContactForm()

    return render(request, "contact.html", {"form": form})

# ======================================== #
# 7. MEDIA GALLERY PAGE                   #
# ======================================== #

def media(request):
    gallery_items = MediaGallery.objects.filter(is_published=True).order_by('sort_order', '-created_at')
    return render(request, 'media.html', {'gallery_items': gallery_items})


# ======================================== #
# 8. GRAPHIC DESIGN PAGE                  #
# ======================================== #

def graphicdesign(request):
    projects = GraphicDesignProject.objects.filter(is_published=True).order_by('sort_order', '-created_at')
    return render(request, 'graphicdesign.html', {'design_projects': projects})


# ======================================== #
# 9. SOCIAL MEDIA MANAGEMENT PAGE         #
# ======================================== #

def smm(request):
    projects = SMMProject.objects.filter(is_published=True).order_by('sort_order', '-created_at')
    return render(request, 'smm.html', {'smm_projects': projects})


# ======================================== #
# 10. WEB DEVELOPMENT PAGE                #
# ======================================== #

def website(request):
    projects = WebProject.objects.filter(is_published=True).order_by('sort_order', '-created_at')
    return render(request, 'website.html', {'web_projects': projects})


# ======================================== #
# 11. MOBILE APP PAGE                     #
# ======================================== #

def mobileapp(request):
    projects = MobileAppProject.objects.filter(is_published=True).order_by('sort_order', '-created_at')
    return render(request, 'mobileapp.html', {'mobile_projects': projects})


# ======================================== #
# 12. DATABASE SERVICES PAGE              #
# ======================================== #

def database(request):
    projects = DatabaseProject.objects.filter(is_published=True).order_by('sort_order', '-created_at')
    return render(request, 'database.html', {'database_projects': projects})


# ======================================== #
# 13. SHOP PAGE                           #
# ======================================== #

def shop(request):
    products = ShopProduct.objects.filter(is_published=True).order_by('sort_order', '-created_at')
    return render(request, 'shop.html', {'products': products})


# ======================================== #
# 14. DECORE PAGE                         #
# ======================================== #

def decore(request):
    projects = DecoreProject.objects.filter(is_published=True).order_by('sort_order', '-created_at')
    return render(request, 'decore.html', {'decore_projects': projects})

# ======================================== #
# 16. AUTHENTICATION VIEWS                #
# ======================================== #

def logout_user(request):
    logout(request)
    messages.success(request, _('You have been logged out successfully.'))
    return redirect('index')


def login_user(request):
    if request.user.is_authenticated:
        messages.info(request, _("You are already logged in."))
        return redirect("index")

    if request.method == "POST":
        username = request.POST.get('username', '').strip()
        password = request.POST.get('password', '').strip()

        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            next_page = request.GET.get('next', 'index')
            
            if '/admin/' in next_page and not user.is_staff:
                messages.error(request, _("You don't have access to the admin panel."))
                return redirect('index')
                
            return redirect(next_page)
        else:
            messages.error(request, _("Invalid username or password."))
    
    return render(request, 'login.html')


def signup_user(request):
    if request.method == "POST":
        form = SignUpForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            email = form.cleaned_data['email']

            if User.objects.filter(username=username).exists():
                form.add_error('username', _("This username is already taken."))
            elif User.objects.filter(email=email).exists():
                form.add_error('email', _("This email is already registered."))
            else:
                user = form.save()
                Profile.objects.get_or_create(user=user)
                login(request, user)
                messages.success(request, _("Your account has been created successfully!"))
                return redirect("index")

        messages.error(request, _("Please check the form for errors."))
        return render(request, 'signup.html', {'form': form})
    else:
        form = SignUpForm()
    return render(request, 'signup.html', {'form': form})


@login_required
def update_user(request):
    current_user = User.objects.get(id=request.user.id)
    user_form = UserUpdateForm(request.POST or None, instance=current_user)
    
    if user_form.is_valid():
        user_form.save()
        login(request, current_user)
        messages.success(request, _('Profile updated successfully!'))
        return redirect('index')
    
    return render(request, 'update_user.html', {'user_form': user_form})


@login_required
def update_password(request):
    current_user = request.user

    if request.method == 'POST':
        form = UpdatePasswordForm(current_user, request.POST)
        if form.is_valid():
            form.save()
            login(request, current_user)
            messages.success(request, _('Password changed successfully.'))
            return redirect('update_user')
        else:
            for error in list(form.errors.values()):
                messages.error(request, error)
    else:
        form = UpdatePasswordForm(current_user)

    return render(request, 'update_password.html', {'form': form})


@login_required
def update_info(request):
    current_user, created = Profile.objects.get_or_create(user=request.user)

    if request.method == "POST":
        form = UpdateUserInfo(request.POST, instance=current_user)
        if form.is_valid():
            form.save()
            messages.success(request, _('Information updated successfully.'))
            return redirect('index')
        else:
            messages.error(request, _('Please check the form for errors.'))
    else:
        form = UpdateUserInfo(instance=current_user)

    return render(request, 'update_info.html', {'form': form})