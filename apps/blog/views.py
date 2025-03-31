from rest_framework.generics import ListAPIView, RetrieveAPIView
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.exceptions import NotFound, APIException
import redis

from django.conf import settings
from django.utils.decorators import method_decorator
from django.views.decorators.cache import cache_page

from .models import Post, Heading, PostView, PostAnalytics
from .serializers import PostListSerializers, PostSerializers, HeadingSerializers
from core.permissions import HasValidAPIKey
from django.core.cache import cache
from .utils import get_client_ip
from .tasks import increment_post_view_task

redis_client = redis.StrictRedis(host=settings.REDIS_HOST, port=6379, db=0)

    
class PostListView(APIView):
    permission_classes = [HasValidAPIKey]
    
    def get(self, request, *args, **kwargs):
        try:
            # Verifica si existe el caché
            cached_posts = cache.get('posts_list')
            
            if cached_posts:
                # Incrementa las impresiones en Redis para los Posts del caché
                for post in cached_posts:
                    redis_client.incr(f'post:impressions:{post["id"]}')
                return Response(cached_posts)
            
    
            # Si no está en caché, obtener los posts de base de datos
            posts = Post.postobjects.all()
            if not posts.exists():
                raise NotFound(detail='No posts found')

            # Serializa los datos
            serializad_posts = PostListSerializers(posts, many=True).data
            
            # Guarda en caché los posts por 5 minutos
            cache.set('posts_list', serializad_posts, timeout=2)
            
            # Incrementa las impresiones para los Posts
            for post in posts:
                redis_client.incr(f'post:impressions:{post.id}')
            
        except Post.DoesNotExist:
            raise NotFound(detail='No posts found')
        return Response(serializad_posts) 

      
class PostDetailView(APIView):
    permission_classes = [HasValidAPIKey]

    def get(self, request, slug, *args, **kwargs): 
        ip_address = get_client_ip(request)    

        try:
            # Verificar si los datos están en caché
            cached_post = cache.get(f'post_detail:{slug}')
            if cached_post:
                # Incrementar vistas del post
                increment_post_view_task.delay(slug, ip_address)
                return Response(cached_post)
            
            # Si no está en caché, obtener el post de la base de datos
            post = Post.objects.get(slug=slug)
            serialized_post = PostSerializers(post).data
            
            # Guardar en el caché
            cache.set(f'post_detail:{slug}', serialized_post, timeout=60)

            # Incrementar vistas en segundo plano
            increment_post_view_task.delay(post.slug, ip_address)

        except Post.DoesNotExist:
            raise NotFound(detail='The requested post does not exist')
        except Exception as e:
            raise APIException(detail=f'An unexpected error ocureed: {str(e)}')

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
        Incrementa el numero de click por Post
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