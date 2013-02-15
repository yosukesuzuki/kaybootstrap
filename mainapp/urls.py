# -*- coding: utf-8 -*-
# mainapp.urls
# 

import urllib

from google.appengine.api import memcache

from kay.routing import (
  ViewGroup, Rule
)
from kay.generics import crud
from kay.generics import admin_required

from adminapp.forms import AdminPageForm
from mainapp.models import AdminPage
from mainapp.views import CACHE_NAME_FOR_TOP_PAGE_RESULTS

view_groups = [
  ViewGroup(
    Rule('/', endpoint='index', view='mainapp.views.index'),
    Rule('/bad/request/', endpoint='bad_request', view='mainapp.views.bad_request'),
    Rule('/article/<string:key_name>/', endpoint='show_each_article', view='mainapp.views.show_each_article'),
    Rule('/article/', endpoint='article_list', view='mainapp.views.article_list'),
    Rule('/tag/<string:tag_name>/', endpoint='search_by_tag', view='mainapp.views.search_by_tag'),
    Rule('/search/', endpoint='search_by_keyword', view='mainapp.views.search_by_keyword'),
    Rule('/rss/feed/', endpoint='rss_feed', view='mainapp.views.rss_feed'),
    Rule('/<string:key_name>/', endpoint='show_each_page', view='mainapp.views.show_each_page'),
  )
]

