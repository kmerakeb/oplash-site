from telnetlib import STATUS
from django.conf import settings
from django.contrib.auth import get_user_model
from django.db import models
from django.urls import reverse
from django.utils.text import slugify
from tinymce.models import HTMLField
from django.db.models import Count


import markdown
from taggit.managers import TaggableManager


class ArticleQuerySet(models.QuerySet):
    def with_favorites(self, user):
        return self.annotate(
            num_favorites=models.Count("favorites"),
            is_favorite=models.Exists(
                get_user_model().objects.filter(
                    pk=user.id, favorites=models.OuterRef("pk")
                ),
            )
            if user.is_authenticated
            else models.Value(False, output_field=models.BooleanField()),
        )
    def get_published(self):
        return self.filter(status="P")

    def get_drafts(self):
        return self.filter(status="D")

    def get_counted_tags(self):
        tag_dict = {}
        query = ( 
            self.filter(status="P").annotate(tagged=Count("tags")).filter(tags__get=0)
        )
        for obj in query:
            for tag in obj. tags.names():
                if tag not in tag_dict:
                    tag_dict[tag]=1
                else:
                    tag_dict[tag] +1
        return tag_dict.items()


ArticleManager = models.Manager.from_queryset(ArticleQuerySet)


   


class Article(models.Model):
    DRAFT ="D"
    PUBLISHED = "P"
    STATUS = ((DRAFT, ("Draft")), (PUBLISHED, ("Published")))

    author = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    title = models.CharField(max_length=120)
    summary = models.TextField(blank=True)
    #content = models.TextField(blank=True)
    thumbnail = models.ImageField()
    featured = models.BooleanField()
    read_time = models.TimeField(null=True, blank=True)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    content = HTMLField('Content')
    status = models.CharField(max_length=1, choices=STATUS, default=DRAFT)
    #draft = models.BooleanField(default=True)
    previous_article = models.ForeignKey('self', related_name='previous', on_delete=models.SET_NULL, blank=True, null=True)
    next_article = models.ForeignKey('self', related_name='next', on_delete=models.SET_NULL, blank=True, null=True)


    tags = TaggableManager(blank=True)

    favorites = models.ManyToManyField(
        settings.AUTH_USER_MODEL, blank=True, related_name="favorites"
    )

    objects = ArticleManager()

    def __str__(self):
        return self.title


    def get_readtime(self):
        from html import unescape
        from django.utils.html import strip_tags

        string = self.title + unescape(strip_tags(self.content))
        total_words = len((string).split())
        return round(total_words / 200)
    
   


    @property
    def slug(self):
        return slugify(self.title)

    def get_absolute_url(self):
        return reverse(
            "articles:detail",
            kwargs={
                "pk": self.id,
                "slug": self.slug,
            },
        )

    def as_markdown(self):
        return markdown.markdown(self.content, safe_mode="escape", extensions=["extra"])
