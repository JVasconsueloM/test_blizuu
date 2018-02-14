from django.test import TestCase

# Create your tests here.
from apps.comun.models import GitLog, GitLogDetails
from apps.comun.utils import QueryGithub


class GitTestCase(TestCase):
    def test_request_successful(self):
        git = QueryGithub()
        git.get_repositories()
        self.assertEqual(git.response.ok, True)
        self.assertEqual(git.response.status_code, 200)
        self.assertEqual(type(git.get_repositories()), type([]))
        print(type(git.get_repositories()), type([]))

    def test_log_created_successful(self):
        git = QueryGithub()
        data_responsed = git.get_repositories()
        parent = GitLog.objects.filter(url_queried='https://api.github.com/search/repositories')
        childs = GitLogDetails.objects.filter(gitlog=parent)
        self.assertIs(parent.exists(), True)
        self.assertIs(len(childs), len(data_responsed[-10:]))
