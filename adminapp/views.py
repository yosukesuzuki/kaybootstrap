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
import werkzeug
from werkzeug import Response

from google.appengine.api import files
from google.appengine.api import memcache
from google.appengine.ext import blobstore

from kay import utils
from kay.utils import render_to_response
from kay.utils import get_by_key_name_or_404
from kay.i18n import gettext as _
from kay.auth.decorators import admin_required
from kay.handlers import blobstore_handlers

from mainapp.views import CACHE_NAME_FOR_TOP_PAGE_RESULTS
from mainapp.models import AdminPage,BlobStoreImages
from adminapp.forms import AdminPageForm

# Create your views here.

def index(request):
    admin_page_list = [{'title':_('Page Manager'),'info':AdminPage.__doc__,'url':'adminpage'},
            {'title':_('Image Manager'),'info':BlobStoreImages.__doc__,'url':'blobstoreimages'}]
    return render_to_response('adminapp/index.html', {'admin_page_list': admin_page_list})

def image_manager(request):
    return render_to_response('adminapp/image_manager.html', {'title':_('Image manager')})

def update_page_order(request):
    try:
        new_orders = request.args['orders']
    except:
        return Response('Error:no data')
    new_orders_list = new_orders.split(';')
    new_order_incre = 0
    for new_order in new_orders_list:
        if new_order is None or new_order == '':
            continue
        new_order_key_name = new_order[5:]
        new_order_entity = AdminPage.get_by_key_name(new_order_key_name)
        if new_order_entity:
            new_order_entity.page_order = new_order_incre 
            new_order_incre += 1
            new_order_entity.put()
    memcache.delete(CACHE_NAME_FOR_TOP_PAGE_RESULTS)
    return Response('Success:new order was saved,'+str(new_order_incre)+' times')

def image_upload_url(request):
    upload_url = blobstore.create_upload_url('/admin/image/upload/handler/')
    return Response('"'+upload_url+'"',mimetype='application/json')

class UploadHandler(blobstore_handlers.BlobstoreUploadHandler):
  def post(self):
    upload_files = self.get_uploads('files')  # 'file' is file upload field in the form
    logging.info('files:'+str(len(upload_files)))
    for uf in upload_files:
        bsi_entity = BlobStoreImages(blob_key=uf.key())
        bsi_entity.put()
    headers = {} 
    return werkzeug.Response('success', headers=headers, status=200)

