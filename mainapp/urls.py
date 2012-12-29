# -*- coding: utf-8 -*-
# mainapp.urls
# 

from kay.routing import (
  ViewGroup, Rule
)

view_groups = [
  ViewGroup(
    Rule('/', endpoint='index', view='mainapp.views.index'),
  )
]

