from django.views.generic import FormView
from django.core.urlresolvers import reverse, reverse_lazy

from apps.comun.constants import CREATED_DATE
from apps.comun.forms import GitHubRepositoriesForm
from apps.comun.utils import build_url


class GitHubRepositoriesView(FormView):
    template_name = 'base.html'
    form_class = GitHubRepositoriesForm
    success_url = reverse_lazy('comun:git_repositories_list')

    def dispatch(self, request, *args, **kwargs):
        self.q = self.request.GET.get('search', '')
        self.sort = self.request.GET.get('sort', CREATED_DATE)
        return super(GitHubRepositoriesView, self).dispatch(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super(GitHubRepositoriesView, self).get_context_data(**kwargs)
        from apps.comun.utils import QueryGithub
        git = QueryGithub(sort=self.sort, q=self.q)
        context['object_list'] = git.get_repositories()

        return context

    def get_initial(self):
        return {
            'busqueda': self.q,
            'orden': self.sort,
        }

    def form_valid(self, form):
        self.success_url = build_url('comun:git_repositories_list', params=form.get_params())
        return super(GitHubRepositoriesView, self).form_valid(form)
