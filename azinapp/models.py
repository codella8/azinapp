from django.db import models
from django.utils.translation import gettext_lazy as _

class Work(models.Model):
    name = models.CharField(max_length=300 , verbose_name=_('Project Name'))
    description = models.TextField(verbose_name=_('Description'))
    image = models.ImageField(upload_to='works/')
    created_at = models.DateTimeField(auto_now_add=True)
    url = models.URLField(verbose_name=_('Project URL'), blank=True, null=True)

    def __str__(self):
        return self.name
    
class Team(models.Model):
    name = models.CharField(max_length=100, verbose_name="name")
    role = models.CharField(max_length=100, verbose_name="Job")
    bio = models.TextField(verbose_name="short discription", blank=True, null=True)
    photo = models.ImageField(upload_to="team/", verbose_name="profile picture")

    instagram = models.URLField(blank=True, null=True)
    linkedin = models.URLField(blank=True, null=True)
    github = models.URLField(blank=True, null=True)

    class Meta:
        verbose_name = "team member"
        verbose_name_plural = "team members"

    def __str__(self):
        return self.name

class Contact(models.Model):
    name = models.CharField(max_length=100, verbose_name="Name")
    email = models.EmailField(verbose_name="Email")
    message = models.TextField(verbose_name="Massage")
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = "ContactMassage"
        verbose_name_plural = "ContactMassages"

    def __str__(self):
        return f"{self.name} - {self.email}"