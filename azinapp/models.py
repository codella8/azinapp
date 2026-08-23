from django.db import models
from django.utils.text import slugify
from django.utils.translation import gettext_lazy as _
from django.contrib.auth.models import User


# ======================================== #
# 1. USER PROFILE                         #
# ======================================== #

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, null=True, blank=True)
    date_modified = models.DateTimeField(auto_now=True)
    phone = models.CharField(max_length=25, blank=True)
    address1 = models.CharField(max_length=250, blank=True)
    address2 = models.CharField(max_length=250, blank=True)
    city = models.CharField(max_length=25, blank=True)
    state = models.CharField(max_length=25, blank=True)
    zipcode = models.CharField(max_length=25, blank=True)
    country = models.CharField(max_length=25, default='IRAN')
    old_cart = models.CharField(max_length=200, blank=True, null=True)
    
    def __str__(self):
        return self.user.username


# ======================================== #
# 2. TEAM MEMBERS                         #
# ======================================== #

class Team(models.Model):
    name = models.CharField(max_length=100, verbose_name="Name")
    role = models.CharField(max_length=100, verbose_name="Job Title")
    bio = models.TextField(verbose_name="Short Description", blank=True, null=True)
    photo = models.ImageField(upload_to="team/", verbose_name="Profile Picture")

    instagram = models.URLField(blank=True, null=True)
    linkedin = models.URLField(blank=True, null=True)
    github = models.URLField(blank=True, null=True)

    class Meta:
        verbose_name = "Team Member"
        verbose_name_plural = "Team Members"
        ordering = ['name']

    def __str__(self):
        return self.name


# ======================================== #
# 3. CONTACT MESSAGES                     #
# ======================================== #

class Contact(models.Model):
    name = models.CharField(max_length=100, verbose_name="Name")
    email = models.EmailField(verbose_name="Email")
    message = models.TextField(verbose_name="Message")
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = "Contact Message"
        verbose_name_plural = "Contact Messages"
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.name} - {self.email}" 


# ======================================== #
# 5. MEDIA GALLERY (AZIN MEDIA)           #
# ======================================== #

class MediaGallery(models.Model):
    CATEGORY_CHOICES = (
        ('wedding', 'Wedding'),
        ('birthday', 'Birthday'),
        ('product', 'Product Photography'),
        ('corporate', 'Corporate Events'),
        ('portrait', 'Portrait'),
        ('other', 'Other'),
    )
    
    title = models.CharField(max_length=200, verbose_name="Title")
    description = models.TextField(blank=True, verbose_name="Description")
    category = models.CharField(max_length=50, choices=CATEGORY_CHOICES, default='other')
    file = models.FileField(upload_to='media_gallery/', verbose_name="Image or Video")
    thumbnail = models.ImageField(upload_to='media_gallery/thumbnails/', blank=True, null=True, verbose_name="Thumbnail")
    is_video = models.BooleanField(default=False, verbose_name="Is Video")
    is_featured = models.BooleanField(default=False, verbose_name="Featured")
    is_published = models.BooleanField(default=True, verbose_name="Published")
    sort_order = models.PositiveIntegerField(default=0, verbose_name="Sort Order")
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        ordering = ['sort_order', '-created_at']
        verbose_name = "Gallery Item"
        verbose_name_plural = "Gallery Items"
    
    def __str__(self):
        return self.title


# ======================================== #
# 6. GRAPHIC DESIGN PROJECTS              #
# ======================================== #

class GraphicDesignProject(models.Model):
    CATEGORY_CHOICES = (
        ('logo', 'Logo Design'),
        ('branding', 'Brand Identity'),
        ('motion', 'Motion Graphics'),
        ('packaging', 'Packaging Design'),
        ('print', 'Print Design'),
        ('social', 'Social Media Graphics'),
        ('other', 'Other'),
    )
    
    title = models.CharField(max_length=200, verbose_name="Project Title")
    slug = models.SlugField(unique=True, blank=True, verbose_name="Slug")
    description = models.TextField(verbose_name="Description")
    short_description = models.TextField(blank=True, verbose_name="Short Description")
    category = models.CharField(max_length=50, choices=CATEGORY_CHOICES, default='other')
    client = models.CharField(max_length=200, blank=True, verbose_name="Client Name")
    image = models.ImageField(upload_to='graphic_projects/', verbose_name="Main Image")
    gallery = models.ManyToManyField('GraphicProjectImage', blank=True, verbose_name="Gallery")
    is_featured = models.BooleanField(default=False, verbose_name="Featured Project")
    is_published = models.BooleanField(default=True, verbose_name="Published")
    sort_order = models.PositiveIntegerField(default=0, verbose_name="Sort Order")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ['sort_order', '-created_at']
        verbose_name = "Graphic Design Project"
        verbose_name_plural = "Graphic Design Projects"
    
    def __str__(self):
        return self.title
    
    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title)
        super().save(*args, **kwargs)


class GraphicProjectImage(models.Model):
    project = models.ForeignKey(GraphicDesignProject, on_delete=models.CASCADE, related_name='images')
    image = models.ImageField(upload_to='graphic_projects/gallery/')
    caption = models.CharField(max_length=200, blank=True)
    sort_order = models.PositiveIntegerField(default=0)
    
    class Meta:
        ordering = ['sort_order']
        verbose_name = "Gallery Image"
        verbose_name_plural = "Gallery Images"
    
    def __str__(self):
        return f"{self.project.title} - Image {self.sort_order}"


# ======================================== #
# 7. SOCIAL MEDIA MANAGEMENT (SMM)        #
# ======================================== #

class SMMProject(models.Model):
    CATEGORY_CHOICES = (
        ('reel', 'Reels & Short Videos'),
        ('ad', 'Advertising Clips'),
        ('content', 'Content Production'),
        ('campaign', 'Marketing Campaigns'),
        ('story', 'Story Management'),
        ('other', 'Other'),
    )
    
    PLATFORM_CHOICES = (
        ('instagram', 'Instagram'),
        ('facebook', 'Facebook'),
        ('tiktok', 'TikTok'),
        ('youtube', 'YouTube'),
        ('linkedin', 'LinkedIn'),
        ('telegram', 'Telegram'),
        ('other', 'Other'),
    )
    
    title = models.CharField(max_length=200, verbose_name="Project Title")
    slug = models.SlugField(unique=True, blank=True, verbose_name="Slug")
    description = models.TextField(verbose_name="Description")
    short_description = models.TextField(blank=True, verbose_name="Short Description")
    category = models.CharField(max_length=50, choices=CATEGORY_CHOICES, default='other', verbose_name="Category")
    platform = models.CharField(max_length=50, choices=PLATFORM_CHOICES, blank=True, verbose_name="Platform")
    client = models.CharField(max_length=200, blank=True, verbose_name="Client Name")
    
    # Media
    image = models.ImageField(upload_to='smm_projects/', verbose_name="Cover Image")
    is_video = models.BooleanField(default=False, verbose_name="Is Video")
    video_url = models.URLField(blank=True, null=True, verbose_name="Video URL (YouTube/Vimeo)")
    video_file = models.FileField(upload_to='smm_projects/videos/', blank=True, null=True, verbose_name="Video File")
    
    # Gallery
    gallery = models.ManyToManyField('SMMProjectImage', blank=True, verbose_name="Gallery")
    
    # Statistics
    reach = models.CharField(max_length=100, blank=True, verbose_name="Reach / Views")
    engagement = models.CharField(max_length=100, blank=True, verbose_name="Engagement")
    likes = models.CharField(max_length=100, blank=True, verbose_name="Likes")
    shares = models.CharField(max_length=100, blank=True, verbose_name="Shares")
    comments = models.CharField(max_length=100, blank=True, verbose_name="Comments")
    
    # Status
    is_featured = models.BooleanField(default=False, verbose_name="Featured Project")
    is_published = models.BooleanField(default=True, verbose_name="Published")
    sort_order = models.PositiveIntegerField(default=0, verbose_name="Sort Order")
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ['sort_order', '-created_at']
        verbose_name = "SMM Project"
        verbose_name_plural = "SMM Projects"
    
    def __str__(self):
        return self.title
    
    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title)
        super().save(*args, **kwargs)


class SMMProjectImage(models.Model):
    project = models.ForeignKey(SMMProject, on_delete=models.CASCADE, related_name='project_images')
    image = models.ImageField(upload_to='smm_projects/gallery/', verbose_name="Gallery Image")
    caption = models.CharField(max_length=200, blank=True, verbose_name="Caption")
    sort_order = models.PositiveIntegerField(default=0, verbose_name="Sort Order")
    
    class Meta:
        ordering = ['sort_order']
        verbose_name = "SMM Gallery Image"
        verbose_name_plural = "SMM Gallery Images"
    
    def __str__(self):
        return f"{self.project.title} - {self.sort_order}"


class SMMClient(models.Model):
    name = models.CharField(max_length=200, verbose_name="Client Name")
    logo = models.ImageField(upload_to='smm_clients/', blank=True, null=True, verbose_name="Logo")
    website = models.URLField(blank=True, null=True, verbose_name="Website")
    industry = models.CharField(max_length=200, blank=True, verbose_name="Industry")
    is_active = models.BooleanField(default=True, verbose_name="Active")
    
    class Meta:
        verbose_name = "SMM Client"
        verbose_name_plural = "SMM Clients"
        ordering = ['name']
    
    def __str__(self):
        return self.name


# ======================================== #
# 8. WEB DEVELOPMENT PROJECTS             #
# ======================================== #

class WebProject(models.Model):
    CATEGORY_CHOICES = (
        ('corporate', 'Corporate Website'),
        ('ecommerce', 'E-Commerce'),
        ('saas', 'SaaS Platform'),
        ('portfolio', 'Portfolio Site'),
        ('blog', 'Blog & News'),
        ('custom', 'Custom Web App'),
        ('erp system', 'ERP System'),
        ('other', 'Other'),
    )
    
    title = models.CharField(max_length=200, verbose_name="Project Title")
    slug = models.SlugField(unique=True, blank=True, verbose_name="Slug")
    description = models.TextField(verbose_name="Description")
    short_description = models.TextField(blank=True, verbose_name="Short Description")
    category = models.CharField(max_length=50, choices=CATEGORY_CHOICES, default='other', verbose_name="Category")
    client = models.CharField(max_length=200, blank=True, verbose_name="Client Name")
    
    # Media
    image = models.ImageField(upload_to='web_projects/', verbose_name="Cover Image")
    gallery = models.ManyToManyField('WebProjectImage', blank=True, verbose_name="Gallery")
    
    # Technical Details
    technologies = models.CharField(max_length=500, blank=True, verbose_name="Technologies Used")
    features = models.TextField(blank=True, verbose_name="Key Features")
    live_url = models.URLField(blank=True, null=True, verbose_name="Live URL")
    
    # Status
    is_featured = models.BooleanField(default=False, verbose_name="Featured Project")
    is_published = models.BooleanField(default=True, verbose_name="Published")
    sort_order = models.PositiveIntegerField(default=0, verbose_name="Sort Order")
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ['sort_order', '-created_at']
        verbose_name = "Web Project"
        verbose_name_plural = "Web Projects"
    
    def __str__(self):
        return self.title
    
    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title)
        super().save(*args, **kwargs)


class WebProjectImage(models.Model):
    project = models.ForeignKey(WebProject, on_delete=models.CASCADE, related_name='project_images')
    image = models.ImageField(upload_to='web_projects/gallery/', verbose_name="Gallery Image")
    caption = models.CharField(max_length=200, blank=True, verbose_name="Caption")
    sort_order = models.PositiveIntegerField(default=0, verbose_name="Sort Order")
    
    class Meta:
        ordering = ['sort_order']
        verbose_name = "Web Project Image"
        verbose_name_plural = "Web Project Images"
    
    def __str__(self):
        return f"{self.project.title} - {self.sort_order}"


# ======================================== #
# 9. MOBILE APP PROJECTS                  #
# ======================================== #

class MobileAppProject(models.Model):
    CATEGORY_CHOICES = (
        ('ios', 'iOS App'),
        ('android', 'Android App'),
        ('cross', 'Cross-Platform'),
        ('hybrid', 'Hybrid App'),
        ('other', 'Other'),
    )
    
    title = models.CharField(max_length=200, verbose_name="Project Title")
    slug = models.SlugField(unique=True, blank=True, verbose_name="Slug")
    description = models.TextField(verbose_name="Description")
    short_description = models.TextField(blank=True, verbose_name="Short Description")
    category = models.CharField(max_length=50, choices=CATEGORY_CHOICES, default='other', verbose_name="Category")
    client = models.CharField(max_length=200, blank=True, verbose_name="Client Name")
    
    # Media
    image = models.ImageField(upload_to='mobile_projects/', verbose_name="Cover Image")
    gallery = models.ManyToManyField('MobileAppImage', blank=True, verbose_name="Gallery")
    
    # Technical Details
    platform = models.CharField(max_length=200, blank=True, verbose_name="Platform")
    technologies = models.CharField(max_length=500, blank=True, verbose_name="Technologies Used")
    features = models.TextField(blank=True, verbose_name="Key Features")
    app_store_url = models.URLField(blank=True, null=True, verbose_name="App Store URL")
    play_store_url = models.URLField(blank=True, null=True, verbose_name="Play Store URL")
    
    # Status
    is_featured = models.BooleanField(default=False, verbose_name="Featured Project")
    is_published = models.BooleanField(default=True, verbose_name="Published")
    sort_order = models.PositiveIntegerField(default=0, verbose_name="Sort Order")
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ['sort_order', '-created_at']
        verbose_name = "Mobile App Project"
        verbose_name_plural = "Mobile App Projects"
    
    def __str__(self):
        return self.title
    
    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title)
        super().save(*args, **kwargs)


class MobileAppImage(models.Model):
    project = models.ForeignKey(MobileAppProject, on_delete=models.CASCADE, related_name='project_images')
    image = models.ImageField(upload_to='mobile_projects/gallery/', verbose_name="Gallery Image")
    caption = models.CharField(max_length=200, blank=True, verbose_name="Caption")
    sort_order = models.PositiveIntegerField(default=0, verbose_name="Sort Order")
    
    class Meta:
        ordering = ['sort_order']
        verbose_name = "Mobile App Image"
        verbose_name_plural = "Mobile App Images"
    
    def __str__(self):
        return f"{self.project.title} - {self.sort_order}"


# ======================================== #
# 10. DATABASE PROJECTS                   #
# ======================================== #

class DatabaseProject(models.Model):
    CATEGORY_CHOICES = (
        ('design', 'Database Design'),
        ('migration', 'Migration'),
        ('optimization', 'Optimization'),
        ('management', 'Management'),
        ('security', 'Security'),
        ('other', 'Other'),
    )
    
    title = models.CharField(max_length=200, verbose_name="Project Title")
    slug = models.SlugField(unique=True, blank=True, verbose_name="Slug")
    description = models.TextField(verbose_name="Description")
    short_description = models.TextField(blank=True, verbose_name="Short Description")
    category = models.CharField(max_length=50, choices=CATEGORY_CHOICES, default='other', verbose_name="Category")
    client = models.CharField(max_length=200, blank=True, verbose_name="Client Name")
    
    # Media
    image = models.ImageField(upload_to='database_projects/', verbose_name="Cover Image")
    gallery = models.ManyToManyField('DatabaseProjectImage', blank=True, verbose_name="Gallery")
    
    # Technical Details
    database_type = models.CharField(max_length=200, blank=True, verbose_name="Database Type")
    technologies = models.CharField(max_length=500, blank=True, verbose_name="Technologies Used")
    features = models.TextField(blank=True, verbose_name="Key Features")
    
    # Status
    is_featured = models.BooleanField(default=False, verbose_name="Featured Project")
    is_published = models.BooleanField(default=True, verbose_name="Published")
    sort_order = models.PositiveIntegerField(default=0, verbose_name="Sort Order")
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ['sort_order', '-created_at']
        verbose_name = "Database Project"
        verbose_name_plural = "Database Projects"
    
    def __str__(self):
        return self.title
    
    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title)
        super().save(*args, **kwargs)


class DatabaseProjectImage(models.Model):
    project = models.ForeignKey(DatabaseProject, on_delete=models.CASCADE, related_name='project_images')
    image = models.ImageField(upload_to='database_projects/gallery/', verbose_name="Gallery Image")
    caption = models.CharField(max_length=200, blank=True, verbose_name="Caption")
    sort_order = models.PositiveIntegerField(default=0, verbose_name="Sort Order")
    
    class Meta:
        ordering = ['sort_order']
        verbose_name = "Database Project Image"
        verbose_name_plural = "Database Project Images"
    
    def __str__(self):
        return f"{self.project.title} - {self.sort_order}"


# ======================================== #
# 11. SHOP PRODUCTS                       #
# ======================================== #

class ShopProduct(models.Model):
    CATEGORY_CHOICES = (
        ('digital', 'Digital Products'),
        ('physical', 'Physical Products'),
        ('service', 'Services'),
        ('other', 'Other'),
    )
    
    title = models.CharField(max_length=200, verbose_name="Product Name")
    slug = models.SlugField(unique=True, blank=True, verbose_name="Slug")
    description = models.TextField(verbose_name="Description")
    short_description = models.TextField(blank=True, verbose_name="Short Description")
    category = models.CharField(max_length=50, choices=CATEGORY_CHOICES, default='other', verbose_name="Category")
    
    # Media
    image = models.ImageField(upload_to='shop_products/', verbose_name="Product Image")
    gallery = models.ManyToManyField('ShopProductImage', blank=True, verbose_name="Gallery")
    
    is_featured = models.BooleanField(default=False, verbose_name="Featured Product")
    is_published = models.BooleanField(default=True, verbose_name="Published")
    sort_order = models.PositiveIntegerField(default=0, verbose_name="Sort Order")
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ['sort_order', '-created_at']
        verbose_name = "Shop Product"
        verbose_name_plural = "Shop Products"
    
    def __str__(self):
        return self.title
    
    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title)
        super().save(*args, **kwargs)


class ShopProductImage(models.Model):
    product = models.ForeignKey(ShopProduct, on_delete=models.CASCADE, related_name='product_images')
    image = models.ImageField(upload_to='shop_products/gallery/', verbose_name="Gallery Image")
    caption = models.CharField(max_length=200, blank=True, verbose_name="Caption")
    sort_order = models.PositiveIntegerField(default=0, verbose_name="Sort Order")
    
    class Meta:
        ordering = ['sort_order']
        verbose_name = "Shop Product Image"
        verbose_name_plural = "Shop Product Images"
    
    def __str__(self):
        return f"{self.product.title} - {self.sort_order}"


# ======================================== #
# 12. DECORE PROJECTS                     #
# ======================================== #

class DecoreProject(models.Model):
    CATEGORY_CHOICES = (
        ('residential', 'Residential'),
        ('commercial', 'Commercial'),
        ('office', 'Office'),
        ('restaurant', 'Restaurant & Cafe'),
        ('hotel', 'Hotel & Hospitality'),
        ('retail', 'Retail'),
        ('other', 'Other'),
    )
    
    title = models.CharField(max_length=200, verbose_name="Project Title")
    slug = models.SlugField(unique=True, blank=True, verbose_name="Slug")
    description = models.TextField(verbose_name="Description")
    short_description = models.TextField(blank=True, verbose_name="Short Description")
    category = models.CharField(max_length=50, choices=CATEGORY_CHOICES, default='other', verbose_name="Category")
    client = models.CharField(max_length=200, blank=True, verbose_name="Client Name")
    location = models.CharField(max_length=200, blank=True, verbose_name="Location")
    area = models.CharField(max_length=100, blank=True, verbose_name="Area (sqm)")
    
    # Media
    image = models.ImageField(upload_to='decore_projects/', verbose_name="Cover Image")
    gallery = models.ManyToManyField('DecoreProjectImage', blank=True, verbose_name="Gallery")
    
    # Details
    style = models.CharField(max_length=200, blank=True, verbose_name="Design Style")
    features = models.TextField(blank=True, verbose_name="Key Features")
    
    # Status
    is_featured = models.BooleanField(default=False, verbose_name="Featured Project")
    is_published = models.BooleanField(default=True, verbose_name="Published")
    sort_order = models.PositiveIntegerField(default=0, verbose_name="Sort Order")
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ['sort_order', '-created_at']
        verbose_name = "Decore Project"
        verbose_name_plural = "Decore Projects"
    
    def __str__(self):
        return self.title
    
    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title)
        super().save(*args, **kwargs)


class DecoreProjectImage(models.Model):
    project = models.ForeignKey(DecoreProject, on_delete=models.CASCADE, related_name='project_images')
    image = models.ImageField(upload_to='decore_projects/gallery/', verbose_name="Gallery Image")
    caption = models.CharField(max_length=200, blank=True, verbose_name="Caption")
    sort_order = models.PositiveIntegerField(default=0, verbose_name="Sort Order")
    
    class Meta:
        ordering = ['sort_order']
        verbose_name = "Decore Project Image"
        verbose_name_plural = "Decore Project Images"
    
    def __str__(self):
        return f"{self.project.title} - {self.sort_order}"