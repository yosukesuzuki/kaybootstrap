# -*- coding: utf-8 -*-
"""
adminapp.views
"""

"""
import logging

from google.appengine.api import users
from google.appengine.api import memcache
from werkzeug import (
  unescape, redirect, Response,
)
from werkzeug.exceptions import (
  NotFound, MethodNotAllowed, BadRequest
)

from kay.utils import (
  render_to_response, reverse,
  get_by_key_name_or_404, get_by_id_or_404,
  to_utc, to_local_timezone, url_for, raise_on_dev
)
from kay.i18n import gettext as _
from kay.auth.decorators import login_required

"""
import logging
import json
import werkzeug
import re
RE_REMOVE_HTTP = re.compile(ur'^http:')
from werkzeug import Response

from google.appengine.api import files
from google.appengine.api import memcache
from google.appengine.ext import db 
from google.appengine.ext import blobstore
from google.appengine.api.images import get_serving_url

from kay import utils
from kay.utils import render_to_response
from kay.utils import url_for
from kay.utils.paginator import Paginator, InvalidPage, EmptyPage
from kay.i18n import gettext as _
from kay.auth.decorators import admin_required
from kay.handlers import blobstore_handlers

from mainapp.views import CACHE_NAME_FOR_TOP_PAGE_RESULTS
from mainapp.models import AdminPage,BlobStoreImage
from adminapp.forms import AdminPageForm

# Create your views here.

def index(request):
    admin_page_list = [{'title':_('Page Manager'),'info':AdminPage.__doc__,'url':'/admin/adminpage/list'},
            {'title':_('Image Manager'),'info':BlobStoreImage.__doc__,'url':'/admin/image/manager/'}]
    return render_to_response('adminapp/index.html', {'admin_page_list': admin_page_list})

def update_page_order(request):
    try:
        new_orders = request.form['orders']
    except:
        return Response('Error:no data')
    new_orders_list = new_orders.split(';')
    new_order_incre = 0
    for new_order in new_orders_list:
        if new_order is None or new_order == '':
            continue
        new_order_entity = db.get(new_order) 
        if new_order_entity:
            new_order_entity.page_order = new_order_incre 
            new_order_incre += 1
            new_order_entity.put()
    memcache.delete(CACHE_NAME_FOR_TOP_PAGE_RESULTS)
    return Response('Success:new order was saved,'+str(new_order_incre)+' times')

def image_manager(request):
    #TODO add image search function by full text search
    return render_to_response('adminapp/image_manager.html', {'title':_('Image manager')})

def image_upload_url(request):
    upload_url = blobstore.create_upload_url('/admin/image/upload/handler/')
    return Response('"'+upload_url+'"',mimetype='application/json')

def image_list_json(request):
    #TODO duplication,I have to DRY below code
    blob_info_query = blobstore.BlobInfo.all().order('-creation')
    blob_info_results = blob_info_query.fetch(1000)
    for r in blob_info_results:
        bsi_entity = BlobStoreImage.get_by_key_name(r.md5_hash)
        if bsi_entity is None:
            bsi_entity = BlobStoreImage(key_name=r.md5_hash,file_name=r.filename,blob_key=r.key())
            bsi_entity.put()
    query = BlobStoreImage.all().order('-update')
    pagenator = Paginator(query,10)
    try:
        page = int(request.args.get('page','1'))
    except ValueError:
        page = 1
    try:
        results = pagenator.page(page)
    except (EmptyPage,InvalidPage):
        results = pagenator.page(pagenator.num_pages)
    return_list = []
    for r in results.object_list:
        return_list.append({'key':str(r.key()),
            'id':r.key().name(),
            'title':r.title,
            'file_name':r.file_name,
            'note':r.note,
            'image_path':RE_REMOVE_HTTP.sub('',get_serving_url(r.blob_key.key())),
            'update':str(r.update)[:16]})
    return Response(json.dumps({'images':return_list,
        'current_page':results.number,
        'total_pages':results.paginator.num_pages}, ensure_ascii=False))
    
class UploadHandler(blobstore_handlers.BlobstoreUploadHandler):
    def post(self):
        query = blobstore.BlobInfo.all().order('-creation')
        results = query.fetch(1000)
        for r in results:
            bsi_entity = BlobStoreImage.get_by_key_name(r.md5_hash)
            if bsi_entity is None:
                bsi_entity = BlobStoreImage(key_name=r.md5_hash,file_name=r.filename,blob_key=r.key())
                bsi_entity.put()
        headers = {} 
        return werkzeug.Response('success', headers=headers, status=200)

def image_delete(request,key):
    bsi_entity = BlobStoreImage.get(key)
    bsi_entity.blob_key.delete()
    bsi_entity.delete()
    return Response('success')
