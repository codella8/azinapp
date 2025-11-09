from django.shortcuts import render, redirect
from django.http import HttpResponse
from . models import Work, Team, Profile
from django.contrib import messages
from .forms import ContactForm
from django.core.mail import send_mail
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from . forms import SignUpForm, UserUpdateForm, UpdatePasswordForm, UpdateUserInfo
from django.conf import settings
from django.utils.translation import gettext as _
from django.contrib.auth.decorators import user_passes_test

def admin_only(user): #بررسی اینکه کاربر ادمین هست یا نه
    return user.is_staff 

@user_passes_test(admin_only) #فقط به ادمین‌ها اجازه ورود می‌دهد
def admin_panel(request):
    return redirect('admin:index')

def my_view(request):
    output = _("Welcome to my site.")
    return HttpResponse(output)

def index(request):
    return render(request, 'index.html')

def about(request):
    team = Team.objects.all()
    return render(request, "about.html", {"team": team}) 

def contact(request):
    if request.method == "POST":
        form = ContactForm(request.POST)
        if form.is_valid():
            name = form.cleaned_data["name"]
            email = form.cleaned_data["email"]
            message = form.cleaned_data["message"]

            send_mail(
                subject=f"پیام جدید از {name}",
                message=f"از: {name} <{email}>\n\n{message}",
                from_email=settings.DEFAULT_FROM_EMAIL,
                recipient_list=[settings.DEFAULT_FROM_EMAIL],
                fail_silently=False,
            )

            messages.success(request, "Massage sent successfully!")
            return redirect("contact")
    else:
        form = ContactForm()

    return render(request, "contact.html", {"form": form})

def portfolio(request):
    projects = Work.objects.all().order_by('-created_at') 
    return render(request, 'portfolio.html', {'projects': projects})

def graphicdesign(request):
    return render(request, 'graphicdesign.html')

def mobileapp(request):
    return render(request, 'mobileapp.html')

def media(request):
    return render(request, 'media.html')

def smm(request):
    return render(request, 'smm.html')

def website(request):
    return render(request, 'website.html')

def store(request):
    return render(request, 'store.html')

def decore(request):
    return render(request, 'decore.html')

def travel(request):
    return render(request, 'travel.html')

def sham_about(request):
    return render(request, 'sham_about.html')

def logout_user(request):
    logout(request)
    messages.success(request, _('با موفقیت خارج شدید'))
    return redirect('index')


def login_user(request): # تعریف ویوی ورود
    if request.user.is_authenticated:
        messages.info(request, _("شما قبلاً وارد شده‌اید."))
        return redirect("index") # اینکار باعث جلوگیری از ورود دوباره‌ی کاربران وارد شده می‌شود

    if request.method == "POST": # گرفتن داده ها
        username = request.POST.get('username', '').strip()
        password = request.POST.get('password', '').strip()

        user = authenticate(request, username=username, password=password) # بررسی اعتبار با authenticated

        if user is not None:
            login(request, user)
            next_page = request.GET.get('next', 'index') #اگر کاربر از یک صفحه خاص به login هدایت شده بود next را برمیگرداند
            
            if '/admin/' in next_page and not user.is_staff:
                messages.error(request, _("شما دسترسی به پنل مدیریت ندارید"))
                return redirect('index') # محافظت از صفحه ادمین
                
            return redirect(next_page)
        else:
            messages.error(request, _("نام کاربری یا رمز عبور اشتباه است"))
    
    return render(request, 'login.html')


def signup_user(request):
    if request.method == "POST": # بررسی درخواست از نوع post
        form = SignUpForm(request.POST)
        if form.is_valid(): #فرم وارد شده را اعتبارسنجی می‌کنیم
            username = form.cleaned_data['username']
            email = form.cleaned_data['email']

            if User.objects.filter(username=username).exists(): #بررسی وجود نام کاربری و ایمیل
                form.add_error('username', _("این نام کاربری قبلاً ثبت شده است."))
            elif User.objects.filter(email=email).exists():
                form.add_error('email', _("این ایمیل قبلاً ثبت شده است."))
            else:
                user = form.save()
                Profile.objects.get_or_create(user=user) # ایجاد پروفایل کاربر 
                #get_or_create() بررسی میکند که آیا پروفایل برای این کاربر وجود دارد یا خیر
                login(request, user) # ورود کاربر به حساب
                messages.success(request, _("اکانت شما ساخته شد."))
                return redirect("index")

        messages.error(request, _("لطفاً خطاهای فرم را بررسی و اصلاح کنید.")) #در صورتی که فرم معتبر نباشد
        return render(request, 'signup.html', {'form': form})

    else:
        form = SignUpForm()
    return render(request, 'signup.html', {'form': form})


def update_user(request):
    if request.user.is_authenticated: #ابتدا بررسی می‌کنیم که آیا کاربر وارد شده است یا خیر.
        current_user = User.objects.get(id=request.user.id) # استفاده از request.user.is_authenticated برای بررسی وضعیت ورود
        user_form = UserUpdateForm(request.POST or None, instance = current_user) # استفاده از فرم UserUpdateForm برای بروزرسانی داده‌ها
        if user_form.is_valid(): 
            user_form.save() # ذخیره‌سازی و بروزرسانی اطلاعات
            login(request, current_user) # بروزرسانی اطلاعات کاربر و ورود مجدد به سیستم
            messages.success(request, 'Updated!')
            return redirect('index')
        return render(request, 'update_user.html', {'user_form': user_form})
       
    else:
        messages.error(request, 'login First') # اگر کاربر وارد نشده باشد
        return redirect('index')
    
def update_password(request):
    if not request.user.is_authenticated:
        messages.error(request, _('لطفاً ابتدا وارد شوید.'))
        return redirect('login')

    current_user = request.user

    if request.method == 'POST':
        form = UpdatePasswordForm(current_user, request.POST)
        if form.is_valid():
            form.save()
            login(request, current_user)
            messages.success(request, 'رمز عبور با موفقیت تغییر کرد.')
            return redirect('update_user')
        else:
            for error in list(form.errors.values()):
                messages.error(request, error)
    else:
        form = UpdatePasswordForm(current_user)

    return render(request, 'update_password.html', {'form': form})


def update_info(request):
    if not request.user.is_authenticated:
        messages.error(request, _('لطفاً ابتدا وارد حساب کاربری شوید.'))
        return redirect('login')

    current_user, created = Profile.objects.get_or_create(user=request.user) # اطلاعات کاربر ساخته شده را ذخیره میکنیم تا در مراحل بعدی استفاده کنیم

    if request.method == "POST":
        form = UpdateUserInfo(request.POST, instance=current_user)
        if form.is_valid():
            form.save()
            messages.success(request, _('اطلاعات با موفقیت بروزرسانی شد.'))
            return redirect('index')
        else:
            messages.error(request, _('Error'))
    else:
        form = UpdateUserInfo(instance=current_user) # نمایش یک فرم خالی برای کاربر و وارد کردن اطلاعات

    return render(request, 'update_info.html', {'form': form})