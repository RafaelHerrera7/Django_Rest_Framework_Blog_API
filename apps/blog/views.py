from rest_framework.generics import ListAPIView, RetrieveAPIView
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.exceptions import NotFound, APIException
import redis
from django.conf import settings

from .models import Post, Heading, PostView, PostAnalytics
from .serializers import PostListSerializers, PostSerializers, HeadingSerializers
from core.permissions import HasValidAPIKey

redis_client = redis.StrictRedis(host=settings.REDIS_HOST, port=6379, db=0)

    
class PostListView(APIView):
    permission_classes = [HasValidAPIKey]
    
    def get(self, request, *args, **kwargs):
        try:
            posts = Post.postobjects.all()

            if not posts.exists():
                raise NotFound(detail='No posts found')

            for post in posts:
                redis_client.incr(f'post:impressions:{post.id}')
                
            serializad_posts = PostListSerializers(posts, many=True).data
            
        except Post.DoesNotExist:
            raise NotFound(detail='No posts found')
        return Response(serializad_posts) 

      
class PostDetailView(APIView):
    permission_classes = [HasValidAPIKey]
        
    def get(self, request, slug, *args, **kwargs): 
        try:
            post = Post.objects.get(slug=slug)
            
        except Post.DoesNotExist:
            raise NotFound(detail='The requested post does not exist')
        except Exception as e:
            raise APIException(detail=f'An unexpected error ocureed: {str(e)}')

        serialized_post = PostSerializers(post).data

        # Increment post view count
        try:
            post_analytics = PostAnalytics.objects.get(post=post)
            post_analytics.incremente_view(request)
        
        except Post.DoesNotExist:
            raise NotFound(detail='Analytics data for this post does not exists')
        except Exception as e:
            raise APIException(detail=f'An error ocureed while updating post analytics: {str(e)}')


        return Response(serialized_post)


class PostHeadingsView(ListAPIView):
    permission_classes = [HasValidAPIKey]
    
    serializer_class = HeadingSerializers
    def get_queryset(self):
        post_slug = self.kwargs.get('slug')
        return Heading.objects.filter(post__slug = post_slug)


class IncrementPostClickView(APIView):
    permission_classes = [HasValidAPIKey]
    
    def post(self, request, *args, **kwargs):
        '''
        Increment the count click of one post with the slug
        '''
        slug = request.data.get('slug')       

        try: 
            post = Post.postobjects.get(slug=slug)
        except: 
            raise NotFound(detail='The requested post does not exist') 

        try:
            post_analytics, created = PostAnalytics.objects.get_or_create(post=post)
            post_analytics.increment_click()
        except Exception as e:
            raise APIException(detail=f'An error ocurred while the updating post analytics: {str(e)}')
        
        return Response({
            'message': 'Click incremented successfully', 
            'click': post_analytics.clicks
        })