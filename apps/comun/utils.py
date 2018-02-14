from pip._vendor import requests
import json
from django.core.urlresolvers import reverse
from django.http import QueryDict

class QueryGithub(object):
    def __init__(self, **kwargs):
        self.type_owner = kwargs.pop('type_owner', 'org')
        self.owner = kwargs.pop('owner', 'githubtraining')
        self.sort = kwargs.pop('sort', 'created_at')
        self.field = kwargs.pop('field', 'name')
        self.q = kwargs.pop('q', '')

        # self.url_base = 'https://api.github.com'
        # self.url_repositories = '{0}/{1}/{2}/repos'.format(self.url_base, self.type_owner, self.owner)

    def prepare_url(self):
        return 'https://api.github.com/search/repositories?q= {0} in:{1} {2}:{3} sort:{4}'.format(
            self.q,
            self.field,
            self.type_owner,
            self.owner,
            self.sort
        )

    def get_repositories(self):
        print(self.prepare_url())
        response = requests.get(self.prepare_url())
        return json.loads(response.text).get('items', []) if response.ok else []


def build_url(*args, **kwargs):
    params = kwargs.pop('params', {})
    url = reverse(*args, **kwargs)
    if not params: return url

    qdict = QueryDict('', mutable=True)
    for k, v in params.items():
        if type(v) is list: qdict.setlist(k, v)
        else: qdict[k] = v

    return url + '?' + qdict.urlencode()