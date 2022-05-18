from django.db import models
from django.contrib.auth.models import User
from django.db.models import Sum

news = 'NS'
article = 'AR'

POST_TYPES = [
    (news, 'Новость'),
    (article, 'Статья'),
]


class Author(models.Model):
    user_id = models.OneToOneField(User, on_delete=models.CASCADE)
    rating = models.IntegerField(default=0)

    def update_rating(self):
        rating_post = Post.objects.filter(author_id=self.pk).aggregate(Sum('rating'))['rating__sum'] * 3
        rating_comment = Comment.objects.filter(user_id=self.user_id).aggregate(Sum('rating'))['rating__sum']
        rating_all_comment = Comment.objects.filter(post_id__author_id=self.pk).aggregate(Sum('rating'))['rating__sum']
        self.rating = rating_post + rating_comment + rating_all_comment
        self.save()


class Category(models.Model):
    name = models.CharField(max_length=255, unique=True)


class Post(models.Model):
    types = models.CharField(max_length=2, choices=POST_TYPES, default=news)
    date_create = models.DateTimeField(auto_now_add=True)
    header = models.CharField(max_length=255)
    text = models.TextField()
    rating = models.IntegerField(default=0)
    author_id = models.ForeignKey(Author, on_delete=models.CASCADE)
    categories = models.ManyToManyField(Category, through='PostCategory')

    def like(self):
        self.rating += 1
        self.save()

    def dislike(self):
        self.rating -= 1
        self.save()

    def preview(self):
        return self.text[:124] + '...'

    def __str__(self):
        return self.header


class PostCategory(models.Model):
    post_id = models.ForeignKey(Post, on_delete=models.CASCADE)
    category_id = models.ForeignKey(Category, on_delete=models.CASCADE)


class Comment(models.Model):
    text = models.TextField()
    date_create = models.DateTimeField(auto_now_add=True)
    rating = models.IntegerField(default=0)
    post_id = models.ForeignKey(Post, on_delete=models.CASCADE)
    user_id = models.ForeignKey(User, on_delete=models.CASCADE)

    def like(self):
        self.rating += 1
        self.save()

    def dislike(self):
        self.rating -= 1
        self.save()
