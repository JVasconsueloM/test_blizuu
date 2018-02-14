import datetime

from pip._vendor import requests
import json
from django.core.urlresolvers import reverse
from django.http import QueryDict

from apps.comun.models import GitLog, GitLogDetails


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
        self.response = requests.get(self.prepare_url())
        data = json.loads(self.response.text).get('items', []) if self.response.ok else []
        # there´s an error in the query of the Github API that can not be sorted,
        # so we proceed to perform an order with lambda
        data = sorted(data, key=lambda x: x[self.sort], reverse=True)
        # now create/update log
        self.log('https://api.github.com/search/repositories', data)

        return data

    def log(self, url, data):
        gitlog, created = GitLog.objects.get_or_create(url_queried=url)
        if not created:
            gitlog.last_query_date = datetime.datetime.now()
            gitlog.save()

        # we make a bulk create because it is the fastest way to execute this action
        details = []
        for item in data[-10:]:
            details.append(GitLogDetails(
                gitlog=gitlog,
                repository_id=item['id'],
                repository_name=item['name'],
                repository_html_url=item['html_url'],
                repository_created_at=gt(item['created_at']),
                repository_pushed_at=gt(item['pushed_at']),
                language=item['language'],
            ))
        GitLogDetails.objects.filter(gitlog=gitlog).delete()
        GitLogDetails.objects.bulk_create(details)


def build_url(*args, **kwargs):
    params = kwargs.pop('params', {})
    url = reverse(*args, **kwargs)
    if not params: return url

    qdict = QueryDict('', mutable=True)
    for k, v in params.items():
        if type(v) is list:
            qdict.setlist(k, v)
        else:
            qdict[k] = v

    return url + '?' + qdict.urlencode()


def gt(dt_str):
    dt, _, us = dt_str.partition(".")
    dt = datetime.datetime.strptime(dt, "%Y-%m-%dT%H:%M:%SZ")
    return dt
