from django.db import models

# Create your models here.
from django.db import models

from account.models import MyUser


class Category(models.Model):
    slug = models.SlugField(max_length=50, primary_key=True)
    name = models.CharField(max_length=50, unique=True)
    description = models.CharField(max_length=100, blank=True)

    def __str__(self):
        return self.name


class Post(models.Model):
    author = models.ForeignKey(MyUser, on_delete=models.CASCADE, related_name='posts')
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name='posts')
    title = models.CharField(max_length=150)
    text = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title


class PostImage(models.Model):
    image = models.ImageField(upload_to='posts', blank=True, null=True)
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='images')


class Reply(models.Model):
    problem = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='replies')
    author = models.ForeignKey(MyUser, on_delete=models.CASCADE, related_name='replies')
    body = models.TextField()
    image = models.ImageField(upload_to='reply_images')
    created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.body[:15] + '...'

    class Meta:
        ordering = ('-created',)


class Comment(models.Model):
    comment = models.TextField()
    author = models.ForeignKey(MyUser, on_delete=models.CASCADE, related_name='comments')
    reply = models.ForeignKey(Reply, on_delete=models.CASCADE, related_name='comments')
    created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.comment

    class Meta:
        ordering = ('created',)