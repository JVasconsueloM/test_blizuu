"""blizuu URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.10/topics/http/urls/
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
from django.conf.urls import url, include
from django.contrib import admin
from django.conf.urls.static import static
from blizuu import settings

from apps.comun.views import *
import debug_toolbar

urlpatterns = [
    url(r'^$', GitHubRepositoriesView.as_view(), name='base'),
    url(r'^admin/', admin.site.urls),
    url(r'^comun/', include('apps.comun.urls', namespace='comun')),
    url(r'^__debug__/', include(debug_toolbar.urls)) if settings.DEBUG else '',
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
