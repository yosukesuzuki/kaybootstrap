# -*- coding: utf-8 -*-
# mainapp.urls
# 

import urllib

from kay.routing import (
  ViewGroup, Rule
)
from kay.generics import crud
from kay.generics import admin_required
from mainapp.forms import AdminTopPageForm
from mainapp.models import AdminTopPage 

class AdminTopPageCRUDViewGroup(crud.CRUDViewGroup):
     model = AdminTopPage
     form = AdminTopPageForm
     templates = {
             'show':'mainapp/general_show.html',
             'list':'mainapp/general_list.html',
             'update':'mainapp/general_update.html',
             }
     def get_query(self, request):
         return self.model.all().order('-update')
     def get_additional_context_on_update(self, request, form):
         return {}
     def get_additional_context_on_create(self, request, form):
         key_name = None
         url = None
         try:
             url = request.form['url']
         except:
             pass
         if url:
             key_name = url
         else:
             key_name = urllib.quote(request.form['title'])
         return {'key_name':key_name}
     authorize = admin_required


view_groups = [
  ViewGroup(
    Rule('/', endpoint='index', view='mainapp.views.index'),
  ),
  AdminTopPageCRUDViewGroup(),
]

