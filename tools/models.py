from django.db import models
from django.db import models
from django.utils.text import slugify
from django.contrib.auth import get_user_model
from categories.models import Category

User = get_user_model()

class Language(models.Model):
    name = models.CharField(max_length=50, unique=True)
    slug = models.SlugField(unique=True)
    icon = models.ImageField(upload_to='language_icons/', blank=True, null=True)
    
    class Meta:
        ordering = ['name']
        indexes = [
            models.Index(fields=['slug']),
        ]

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.name

class Tool(models.Model):
    STATUS_CHOICES = (
        ('pending', 'Pending Review'),
        ('approved', 'Approved'),
        ('rejected', 'Rejected'),
    )
    
    name = models.CharField(max_length=200)
    slug = models.SlugField(unique=True)
    description = models.TextField()
    short_description = models.CharField(max_length=500)
    github_url = models.URLField()
    website_url = models.URLField(blank=True, null=True)
    logo = models.ImageField(upload_to='tool_logos/', blank=True, null=True)
    
    categories = models.ManyToManyField(Category, related_name='tools')
    languages = models.ManyToManyField(Language, related_name='tools')
    
    creator = models.ForeignKey(User, on_delete=models.CASCADE, related_name='tools')
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    
    views_count = models.IntegerField(default=0)
    downloads_count = models.IntegerField(default=0)
    stars_count = models.IntegerField(default=0)
    average_rating = models.FloatField(default=0.0)
    
    is_featured = models.BooleanField(default=False)
    last_updated = models.DateTimeField(auto_now=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created_at']
        indexes = [
            models.Index(fields=['slug']),
            models.Index(fields=['status']),
            models.Index(fields=['-created_at']),
            models.Index(fields=['-stars_count']),
        ]

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.name
