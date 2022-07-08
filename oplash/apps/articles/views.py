from multiprocessing import context
from turtle import title
from django.forms import SlugField
from django.shortcuts import redirect
from django.test import tag
from django.views.generic import (
    CreateView,
    DeleteView,
    DetailView,
    ListView,
    UpdateView,
)


from django.db.models import Q
from taggit.models import Tag
from django.shortcuts import render
from oplash.apps.comments.forms import Comment, CommentForm
from oplash.apps.core.mixins import AuthorRequiredMixin, LoginRequiredMixin

from .forms import Article, ArticleForm

def Search(request):
    template_name = "oplash/articles/search_results.html"
    queryset = Article.objects.all()
    query = request.GET.get('s')
    if query:
        queryset = queryset.filter(Q(title__icontains=query) | Q(summary__icontains=query)).distinct()

    context ={
        "queryset": queryset
    }
  
    return render(request, template_name, context)


class ArticleListView(ListView):
    context_object_name = "articles"
    template_name = "oplash/articles/article_list.html"

    def get_queryset(self):
        queryset = (
            Article.objects.select_related("author")
            .get_published()
            .with_favorites(self.request.user)
            .prefetch_related("tags")
            .order_by("-created")
        )

        if tag := self.request.GET.get("tag"):
            return queryset.filter(tags__name__in=[tag])

        if self.request.user.is_authenticated and "own" in self.request.GET:
            return queryset.filter(author=self.request.user)

        return queryset
        
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["tags"] = Tag.objects.all()
        context['latest'] = Article.objects.get_published().order_by('-created')[0:4]
        context['featured'] = Article.objects.get_published().filter(featured=True).order_by('featured')[0:2]
        return context


class ArticleDetailView(DetailView):
    context_object_name = "article"
    template_name = "oplash/articles/article_detail.html"

    def get_queryset(self):
        queryset = Article.objects.select_related("author").with_favorites(
            self.request.user
        )
        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        is_following = self.object.author.following.filter(
            pk=self.request.user.id
        ).exists()
        comments = (
            Comment.objects.filter(article=self.kwargs["pk"])
            .select_related("author")
            .order_by("-created")
        )

        context["is_following"] = is_following
        context["tags"] = Tag.objects.all()
        context["comments"] = comments
        context["comment_form"] = CommentForm()
        context['related']=Article.objects.prefetch_related("tags").order_by("?")[0:4]
        return context

    def post(self, request, *args, **kwargs):
        comment = Comment(
            content=request.POST.get("content"),
            author=self.request.user,
            article=self.get_object(),
        )
        comment.save()
        return self.get(self, request, *args, **kwargs)


class ArticleCreateView(AuthorRequiredMixin, CreateView):
    model = Article
    form_class = ArticleForm
    template_name = "oplash/articles/article_form.html"

    def form_valid(self, form):
        article = form.save(commit=False)
        article.author = self.request.user
        article.save()

        # save tags
        form.save_m2m()

        return super().form_valid(form)


class ArticleUpdateView(AuthorRequiredMixin, UpdateView):
    model = Article
    form_class = ArticleForm
    template_name = "oplash/articles/article_form.html"


class ArticleDeleteView(AuthorRequiredMixin, DeleteView):
    model = Article
    success_url = "/"


class ArticleFavoriteView(LoginRequiredMixin, UpdateView):
    fields = ["favorites"]
    http_method_names = ["post"]

    def get_queryset(self):
        return Article.objects.select_related("author").exclude(
            author=self.request.user
        )

    def post(self, request, *args, **kwargs):
        self.object = self.get_object()
        if self.object.favorites.filter(id=request.user.id).exists():
            self.object.favorites.remove(request.user)
        else:
            self.object.favorites.add(request.user)

        return redirect(self.object.get_absolute_url())
