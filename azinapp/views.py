from django.shortcuts import render, redirect
from django.http import HttpResponse
from . models import Work, Team
from django.contrib import messages
from .forms import ContactForm
from django.core.mail import send_mail
from django.conf import settings
from django.utils.translation import gettext as _


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
    projects_show = Work.objects.all() 
    return render(request, 'portfolio.html', {'projects_show': projects_show})

def services(request):
    return render(request, 'services.html')

def marketing(request):
    return render(request, 'marketing.html')

def bussinessmanage(request):
    return render(request, 'bussinessmanage.html')

def graphicdesign(request):
    return render(request, 'graphicdesign.html')

def mobileapp(request):
    return render(request, 'mobileapp.html')

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



