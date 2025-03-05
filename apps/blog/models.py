import uuid

from django.db import models
from django.utils import timezone
from django.utils.text import slugify

def blog_thumbnail_directory(instance, filename):
    return f'blog/{instance.title}/{filename}'

def category_thumbnail_directory(instance, filename):
    return f'blog_categories/{instance.name}/{filename}'


class Category(models.Model):
    
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    
    parent = models.ForeignKey(
        'self', 
        related_name='children', 
        on_delete=models.CASCADE, 
        blank=True, 
        null=True
        )
    
    name = models.CharField(max_length=256)
    title = models.CharField(max_length=256, blank=True, null=True)
    description = models.TextField()
    thumbnail = models.ImageField(upload_to=category_thumbnail_directory)
    slug = models.CharField(max_length=256)
     
    def __str__(self):
        return self.name       
    
    
class Post(models.Model):
    
    # Show only post with published status
    class PostObjects(models.Manager):
        def get_queryset(self):
            return super().get_queryset().filter(status='published')
        
    status_options = (
        ('draft', 'Draft'),
        ('published', 'Published')
    )
    
    id = models.UUIDField(primary_key=True, default=uuid.uuid4)

    title = models.CharField(max_length=128)
    description = models.CharField(max_length=256)
    content = models.TextField()
    thumbnail = models.ImageField(upload_to=blog_thumbnail_directory)
    
    keyword = models.CharField(max_length=128)
    slug = models.CharField(max_length=128)
    
    category = models.ForeignKey(Category, on_delete=models.PROTECT)
    
    created_at = models.DateTimeField(default=timezone.now)
    updated_at = models.DateTimeField(auto_now=True)
    
    status = models.CharField(max_length=10, choices=status_options, default='draft')
    
    objects = models.Manager() # Default manager
    postobjects = PostObjects() # Custom manager
    
    class Meta:
        ordering = ('status', '-created_at')
        
    def __str__(self):
        return self.title
    
    
class Heading(models.Model):
    
    id = models.UUIDField(primary_key=True, default=uuid.uuid4)

    post = models.ForeignKey(Post, on_delete=models.PROTECT, related_name='headings')
    
    title = models.CharField(max_length=256)
    slug = models.CharField(max_length=256)
    level = models.IntegerField(
        choices=(
            (1, 'H1'),
            (2, 'H2'),
            (3, 'H3'),
            (4, 'H4'),
            (5, 'H5'),
            (6, 'H6'),
        )
    )
    order = models.PositiveIntegerField()
    
    class Meta:
         ordering = ['order']
         
    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title)
        super().save(*args, **kwargs)
            
        
        