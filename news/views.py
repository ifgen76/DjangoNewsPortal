from django.shortcuts import render
from django.views.generic import ListView, DetailView
from .models import Post, POST_TYPES


class PostList(ListView):
    model = Post
    ordering = '-date_create'
    template_name = 'news/postlist.html'
    context_object_name = 'posts'

class Post(DetailView):
    model = Post
    template_name = 'news/post.html'
    context_object_name = 'post'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['cat'] = dict(POST_TYPES)[self.object.types]
        return context
