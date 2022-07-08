"""oplash URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.conf import settings
from django.contrib import admin
from django.urls import include, path
from django.conf.urls.static import static
from oplash.apps.articles.views import Search
from filebrowser.sites import site
from django_comments.feeds import LatestCommentFeed

urlpatterns = [
    path('admin/filebrowser/', site.urls),
    path("", include("oplash.apps.articles.urls")),
    path("", include("oplash.apps.accounts.urls")),
    path("comments/", include("oplash.apps.comments.urls")),
    path(settings.ADMIN_URL, admin.site.urls),
    path('tinymce/', include('tinymce.urls')),
    path("search/", Search, name='search'),
    path('comments/', include('django_comments.urls')),
    path('feeds/latest/', LatestCommentFeed()),
]

"""if settings.DEBUG:
    urlpatterns += [
        path("__debug__/", include("debug_toolbar.urls")),
    ]"""

if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)