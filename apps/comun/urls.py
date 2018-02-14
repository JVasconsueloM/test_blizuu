from django.conf.urls import url, include

from apps.comun.views import *

urlpatterns = [
    url(r'^git/repositories/$', GitHubRepositoriesView.as_view(), name='git_repositories_list'),
]
