from rest_framework import serializers

from .models import Post, Category, Heading, PostView


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
        ] # Serializa los campos que quiera

        
class HeadingSerializers(serializers.ModelSerializer):
    class Meta:
        model = Heading
        fields = [
            'title',
            'slug',
            'level',
            'order',
        ]


class PostViewSerializers(serializers.ModelSerializer):
    class Meta:
        model = PostView
        fields = '__all__' # Serializers all the fields
    
 
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
    view_count = serializers.SerializerMethodField()  
    
    class Meta:
        model = Post
        fields = '__all__' # Serializers all the fields
    
    # The serializer name and the method name need to be the same, without get_
    def get_view_count(self, obj):
        return obj.post_view.count()
    
    
class PostListSerializers(serializers.ModelSerializer):
    category = CategoryListSerializers()
    view_count = serializers.SerializerMethodField()  
    class Meta:
        model = Post
        fields = [
            'id',
            'title',
            'description',
            'thumbnail',
            'slug',
            'category',
            'view_count'
        ]
    
    # The serializer name and the method name need to be the same, without get_
    def get_view_count(self, obj):
        return obj.post_view.count()
    
   