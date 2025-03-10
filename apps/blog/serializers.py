from rest_framework import serializers

from .models import Post, Category, Heading


class CategorySerializers(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = [
            'id',
            'parent',
            'name', 
            'title', 
            'description',  
            'thumbnail', 
            'slug', 
        ] # Serializers only fields i want

        
class HeadingSerializers(serializers.ModelSerializer):
    class Meta:
        model = Heading
        fields = [
            'title',
            'slug',
            'level',
            'order',
        ]


class CategoryListSerializers(serializers.ModelSerializer):    
    class Meta:
        model = Category
        fields = [
            'name',
            'slug',
        ]        
        

class PostSerializers(serializers.ModelSerializer):
    category = CategoryListSerializers()
    headings = HeadingSerializers(many=True)
    class Meta:
        model = Post
        fields = '__all__' # Serializers all the fields
    
    
class PostListSerializers(serializers.ModelSerializer):
    category = CategoryListSerializers()
    class Meta:
        model = Post
        fields = [
            'id',
            'title',
            'description',
            'thumbnail',
            'slug',
            'category',
        ]
    
