from rest_framework.generics import ListAPIView, RetrieveAPIView
from rest_framework.views import APIView
from rest_framework.response import Response

from .models import Post, Heading, PostView, PostAnalytics
from .serializers import PostListSerializers, PostSerializers, HeadingSerializers
from .utils import get_client_ip

# class PostListView(ListAPIView):
#     queryset = Post.postobjects.all()
#     serializer_class = PostListSerializers
    
class PostListView(APIView):
    def get(self, request, *args, **kwargs):
        posts = Post.postobjects.all()
        serializad_posts = PostListSerializers(posts, many=True).data
        return Response(serializad_posts) 

# class PostDetailView(RetrieveAPIView):
#     queryset = Post.postobjects.all()
#     serializer_class = PostSerializers
#     lookup_field = 'slug'

      
class PostDetailView(APIView):
    def get(self, request, slug, *args, **kwargs): 
        post = Post.objects.get(slug=slug)
        serialized_post = PostSerializers(post).data
        
        # Increment post view count
        post_analytics = PostAnalytics.objects.get(post=post)
        post_analytics.incremente_view(request)

        return Response(serialized_post)


class PostHeadingsView(ListAPIView):
    serializer_class = HeadingSerializers
    def get_queryset(self):
        post_slug = self.kwargs.get('slug')
        return Heading.objects.filter(post__slug = post_slug)
    