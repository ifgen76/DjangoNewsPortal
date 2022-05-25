from django.shortcuts import render
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from .models import Post, POST_TYPES
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from django.urls import reverse_lazy
from .filters import *
from .forms import *
from .models import POST_TYPES, news as st_news, article as st_article

paginator_items_count = 2


class PostList(ListView):
    model = Post
    ordering = '-date_create'
    template_name = 'news/postlist.html'
    context_object_name = 'posts'
    paginate_by = paginator_items_count #ограничение вывода на страницу

class PostView(DetailView):
    model = Post
    template_name = 'news/post.html'
    context_object_name = 'post'
    paginate_by = paginator_items_count

    def get_queryset(self):
        queryset = super().get_queryset()
        self.filterset = NewsFilter(self.request.GET, queryset)
        return self.filterset.qs

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['filterset'] = self.filterset
        return context

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['cat'] = dict(POST_TYPES)[self.object.types]
        return context


def search_page(request):
    queryset = Post.objects.all()
    filterset = NewsFilter(request.GET, queryset)
    page = request.GET.get('page')
    paginator = Paginator(filterset.qs, paginator_items_count)
    try:
        f_qs = paginator.get_page(page)
    except PageNotAnInteger:
        f_qs = paginator.get_page(paginator_items_count)
    except EmptyPage:
        f_qs = paginator.get_page(paginator.num_pages)

    context = {
        'posts': f_qs,
        'filterset': filterset,
        'page_obj': f_qs,
        'paginator': paginator,
    }

    return render(request, 'news/search.html', context=context)


class NewsCreate(CreateView):
    form_class = PostForm
    model = Post
    template_name = 'news/post_edit.html'

    def form_valid(self, form):
        news = form.save(commit=False)
        news.types = st_news
        return super().form_valid(form)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Создание новости:'
        return context


class ArticleCreate(CreateView):
    form_class = PostForm
    model = Post
    template_name = 'news/post_edit.html'

    def form_valid(self, form):
        art = form.save(commit=False)
        art.types = st_article
        return super().form_valid(form)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Создание статьи:'
        return context


class PostUpdate(UpdateView):
    form_class = PostForm
    model = Post
    template_name = 'news/post_edit.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Редактирование публикации:'
        return context


class PostDelete(DeleteView):
    model = Post
    template_name = 'news/post_delete.html'
    success_url = reverse_lazy('postlist')
