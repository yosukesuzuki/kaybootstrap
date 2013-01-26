# -*- coding: utf-8 -*-
# adminapp.urls
# 
import urllib
import re
import logging
import json
import datetime

from google.appengine.api import memcache
from google.appengine.api.images import get_serving_url
from kay.routing import (
  ViewGroup, Rule
)
from kay.generics import crud
from kay.generics import admin_required
from kay.generics.rest import RESTViewGroup
from settings import DEFAULT_LANG

from adminapp.forms import AdminPageForm,ArticleForm
from mainapp.models import AdminPage,BlobStoreImage,Article
from mainapp.views import CACHE_NAME_FOR_TOP_PAGE_RESULTS

def construct_image_json_from_content(body):
    re_result = re.compile(ur'image_id:[a-z0-9]+').findall(body)
    image_list = []
    for r in re_result:
        image_id = re.sub(ur'image_id:','',r)
        tmp_image_entity = BlobStoreImage.get_by_key_name(image_id)
        image_list.append({'id':tmp_image_entity.key().name(),
            'title':tmp_image_entity.title,
            'image_path':re.sub('^http:','',get_serving_url(tmp_image_entity.blob_key.key()))})
    json_dic ={'images':image_list}
    return json.dumps(json_dic, ensure_ascii=False)

def construct_datetime_from_string(display_time_string):
    if display_time_string is None or display_time_string == '':
        display_time = datetime.datetime.now()
    else:
        display_time = datetime.datetime.strptime(display_time_string,'%Y-%m-%d %H:%M')
    return display_time

class AdminPageCRUDViewGroup(crud.CRUDViewGroup):
     entities_per_page = 1000 
     model = AdminPage
     form = AdminPageForm
     templates = {
             'show':'adminapp/general_show.html',
             'list':'adminapp/general_list.html',
             'update':'adminapp/general_update.html',
             }
     def get_query(self, request):
         return self.model.all().filter(u'lang =',DEFAULT_LANG).order('page_order')
     def get_additional_context_on_update(self, request, form):
         memcache.delete(CACHE_NAME_FOR_TOP_PAGE_RESULTS)
         logging.info(request.form['content'])
         image_list = construct_image_json_from_content(request.form['content'])
         return {'images':image_list,'lang':DEFAULT_LANG}
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
         image_list = construct_image_json_from_content(request.form['content'])
         memcache.delete(CACHE_NAME_FOR_TOP_PAGE_RESULTS)
         return {'key_name':key_name,'images':image_list,'lang':DEFAULT_LANG}
     authorize = admin_required

class ArticleCRUDViewGroup(crud.CRUDViewGroup):
     entities_per_page = 20 
     model = Article 
     form = ArticleForm
     templates = {
             'show':'adminapp/general_show.html',
             'list':'adminapp/general_list.html',
             'update':'adminapp/general_update.html',
             }
     def get_query(self, request):
         return self.model.all().filter(u'lang =',DEFAULT_LANG).order('-display_time')
     def get_additional_context_on_update(self, request, form):
         logging.info(request.form['content'])
         image_list = construct_image_json_from_content(request.form['content'])
         tag_list = request.form['tags_string'].split(',')
         display_time = construct_datetime_from_string(request.form['display_time'])
         return {'images':image_list,'lang':DEFAULT_LANG,'tags':tag_list,'display_time':display_time}
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
         image_list = construct_image_json_from_content(request.form['content'])
         tag_list = request.form['tags_string'].split(',')
         display_time = construct_datetime_from_string(request.form['display_time'])
         return {'key_name':key_name,'images':image_list,'lang':DEFAULT_LANG,'tags':tag_list,'display_time':display_time}
     authorize = admin_required

class AdminModelsRESTViewGroup(RESTViewGroup):
      models = ['mainapp.models.BlobStoreImage','mainapp.models.AdminPage','mainapp.models.Article']

view_groups = [
  AdminModelsRESTViewGroup(),
  ViewGroup(
    Rule('/', endpoint='index', view='adminapp.views.index'),
    Rule('/update/page/order/', endpoint='update_page_order', view='adminapp.views.update_page_order'),
    Rule('/add/translation/<string:parent_key>', endpoint='add_translation', view='adminapp.views.add_translation'),
    Rule('/get/children/<string:parent_key>', endpoint='get_children', view='adminapp.views.get_children'),
    Rule('/image/manager/', endpoint='image_manager', view='adminapp.views.image_manager'),
    Rule('/image/list/json/', endpoint='image_list_json', view='adminapp.views.image_list_json'),
    Rule('/image/upload/url/', endpoint='image_upload_url', view='adminapp.views.image_upload_url'),
    Rule('/image/upload/handler/', endpoint='upload_handler', view=('adminapp.views.UploadHandler', (), {})),
    Rule('/image/delete/<string:key>', endpoint='image_delete', view='adminapp.views.image_delete'),
  ),
  AdminPageCRUDViewGroup(),
  ArticleCRUDViewGroup(),
]

