from django.contrib import admin

from .models import Category, Post, Heading, PostAnalytics


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'title', 'parent', 'slug')
    search_fields = ('name', 'title', 'description', 'slug')
    prepopulated_fields = {'slug': ('name',)}
    list_filter = ('parent',)
    ordering = ('name',)
    readonly_fields = ('id',)
    list_editable = ('title',)

     
class HeadingInline(admin.TabularInline):
    model = Heading
    extra = 1
    fields = ('title', 'level', 'order', 'slug')
    prepopulated_fields = {'slug': ('title',)}
    ordering = ('order', )
    

@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    list_display = ('title', 'status', 'category', 'created_at', 'updated_at')
    search_fields = ('title', 'description', 'content', 'keywords', 'slug')
    prepopulated_fields = {'slug': ('title',)}
    list_filter = ('status', 'category', 'updated_at', )
    ordering = ('-created_at',)
    readonly_fields = ('id', 'created_at', 'updated_at')
    fieldsets = (
        ('General Information', {
            'fields': ('title', 'description', 'content', 'thumbnail', 'keyword', 'slug', 'category')
        }), 
        ('Status & Dates', {
            'fields': ('status', 'created_at', 'updated_at')
        }), 
    )
    inlines = [HeadingInline]
    
     
@admin.register(PostAnalytics)
class PostAnalyticsAdmin(admin.ModelAdmin):
    list_display = ('post_title', 'views', 'impressions', 'clicks', 'click_through_rate', 'avg_time_on_page')   
    search_fields = ('post__title',)
    readonly_fields = ('post', 'views', 'impressions', 'clicks', 'click_through_rate', 'avg_time_on_page')
    
    def post_title(self, obj):
        return obj.post.title
    
    post_title.short_description = 'Post Title'
    