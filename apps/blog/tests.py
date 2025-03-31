from django.test import TestCase

from .models import Category, Post
# Create your tests here.

class CategoryModelTest(TestCase):
    def setUp(self):
        self.category = Category.objects.create(
            name='Tech',
            title='Technology',
            description='All about technology',
            slug='tech'
        )

    def test_category_creation(self):
        self.assertEqual(str(self.category), 'Tech')
        self.assertEqual(self.category.title, 'Technology')
        
        
class PostModelTest(TestCase):
    def setUp(self):
        self.category = Category.objects.create(
            name='Tech',
            title='Technology',
            description='All about technology',
            slug='tech'
        )

        self.post = Post.objects.create(
            title='Post',
            description='this is a description', 
            content='lorem',
            thumbnail=None,
            keyword='test, post',
            slug='post',
            category=self.category,
            status='published'
        )
    
    def test_post_creation(self):
        self.assertEqual(str(self.post), 'Post')
        self.assertEqual(self.post.category.name, 'Tech')
    
    def test_post_published(self):
        self.assertTrue(Post.postobjects.filter(status='published').exists())