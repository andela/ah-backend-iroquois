"""authors URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.11/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import include
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path

from authors.settings import STATIC_ROOT, STATIC_URL


urlpatterns = [
    path('admin/', admin.site.urls),

    path('api/', include(('authors.apps.authentication.urls', 'authors.apps.authentication'),
                         namespace='authentication')),
    path('api/', include('authors.apps.profiles.urls')),

    # urls for social authentication app
    path('api/social/', include('authors.apps.social_auth.urls')),

    # urls for articles
    path('api/articles/', include('authors.apps.articles.urls')),
    path('api/profiles/', include('authors.apps.profiles.urls')),
]

urlpatterns += static(STATIC_URL, document_root=STATIC_ROOT)
