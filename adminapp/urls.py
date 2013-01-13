# -*- coding: utf-8 -*-
# adminapp.urls
# 
import urllib

from google.appengine.api import memcache
from kay.routing import (
  ViewGroup, Rule
)
from kay.generics import crud
from kay.generics import admin_required
from kay.generics.rest import RESTViewGroup

from adminapp.forms import AdminPageForm
from mainapp.models import AdminPage,BlobStoreImage
from mainapp.views import CACHE_NAME_FOR_TOP_PAGE_RESULTS

class AdminPageCRUDViewGroup(crud.CRUDViewGroup):
     model = AdminPage
     form = AdminPageForm
     templates = {
             'show':'adminapp/general_show.html',
             'list':'adminapp/general_list.html',
             'update':'adminapp/general_update.html',
             }
     def get_query(self, request):
         return self.model.all().order('page_order')
     def get_additional_context_on_update(self, request, form):
         memcache.delete(CACHE_NAME_FOR_TOP_PAGE_RESULTS)
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
         memcache.delete(CACHE_NAME_FOR_TOP_PAGE_RESULTS)
         return {'key_name':key_name}
     authorize = admin_required

class BlobStoreImageRESTViewGroup(RESTViewGroup):
      models = ['mainapp.models.BlobStoreImage']

view_groups = [
  BlobStoreImageRESTViewGroup(),
  ViewGroup(
    Rule('/', endpoint='index', view='adminapp.views.index'),
    Rule('/update/page/order/', endpoint='update_page_order', view='adminapp.views.update_page_order'),
    Rule('/image/manager/', endpoint='image_manager', view='adminapp.views.image_manager'),
    Rule('/image/list/json/', endpoint='image_list_json', view='adminapp.views.image_list_json'),
    Rule('/image/upload/url/', endpoint='image_upload_url', view='adminapp.views.image_upload_url'),
    Rule('/image/upload/handler/', endpoint='upload_handler', view=('adminapp.views.UploadHandler', (), {})),
    Rule('/image/delete/<string:key>', endpoint='image_delete', view='adminapp.views.image_delete'),
  ),
  AdminPageCRUDViewGroup(),
]

