from django.apps import AppConfig


class AzinappConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'azinapp'
    
    def ready(self): # این متد برای لود کردن فایل های سیگنال ها به کار میرود
        import azinapp.signals # برای دریافت سیگنال ها از signals.py
