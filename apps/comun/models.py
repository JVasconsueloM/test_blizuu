from django.db import models


# Create your models here.
class GitLog(models.Model):
    url_queried = models.URLField()
    last_query_date = models.DateTimeField(auto_now_add=True)


class GitLogDetails(models.Model):
    gitlog = models.ForeignKey(GitLog)
    repository_id = models.IntegerField(null=True, blank=True)
    repository_name = models.CharField(max_length=100, null=True, blank=True)
    repository_html_url = models.URLField(null=True, blank=True)
    repository_created_at = models.DateTimeField(null=True, blank=True)
    repository_pushed_at = models.DateTimeField(null=True, blank=True)
    language = models.CharField(max_length=50, null=True, blank=True)
