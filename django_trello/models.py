from __future__ import unicode_literals
import json
from urllib import urlencode
from django.db import models
from django.conf import settings
import requests


API_URL = "https://api.trello.com/1"

# XXX:
API_KEY = "37fff63de896001f05bbb6b527d377d3"



class Unauthorized(Exception):
    pass


class ResourceUnavailable(Exception):
    pass


class TrelloModel(models.Model):
    URL = ""

    user_token = models.ForeignKey("UserToken")
    trello_id = models.CharField(max_length=24)

    def __init__(self, *args, **kwargs):
        super(TrelloModel, self).__init__(*args, **kwargs)
        self._raw_data = None

    class Meta:
        abstract = True

    def save(self, commit=True, sync=True):
        obj = super(TrelloModel, self).save(commit=commit)
        if sync:
            self.upload()
        return obj

    def upload():
        url = self.user_token.construct_url(self.URL)


class UserToken(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL)
    token = models.CharField(max_length=64, default=SAMPLE_TOKEN)

    def construct_url(self, url):
        querystring = urlencode({"token": self.token, "key": API_KEY})
        return "{0}{1}?{2}".format(API_URL, url, querystring)
