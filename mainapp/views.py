# -*- coding: utf-8 -*-
"""
mainapp.views
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
from werkzeug import Response

from google.appengine.api import files
from google.appengine.api import memcache

from kay.utils import render_to_response
from kay.utils import get_by_key_name_or_404
from kay.i18n import gettext as _

from mainapp.models import AdminPage
from mainapp.forms import AdminPageForm

'''
global vars
'''
TOP_PAGE_CONTENT_NUM = 4
CACHE_NAME_FOR_TOP_PAGE_RESULTS = 'top-page-contents'
DUMMY_DATA_FOR_TOP_PAGE = [{'title':'Dummy,first title','snippet':'this is dummy snippet','url':'/first/'},
        {'title':'Dummy,second title','snippet':'this is dummy snippet','url':'/second/'},
        {'title':'Dummy,third title','snippet':'this is dummy snippet','url':'/third/'},
        {'title':'Dummy,fourth title','snippet':'this is dummy snippet','url':'/fourth/'}]

def index(request):
    '''
    top page
    '''
    results = memcache.get(CACHE_NAME_FOR_TOP_PAGE_RESULTS)
    if results is None:
        query_results = AdminPage.all().filter(u'display_page_flg =',True).order('page_order').fetch(limit=TOP_PAGE_CONTENT_NUM)
        results = []
        for r in query_results:
            url = r.external_url if r.external_url else '/'+r.key().name()+'/'
            snippet = r.content[:50]
            results.append({'title':r.title,'snippet':snippet,'url':url})
        if len(results) == 0:results = DUMMY_DATA_FOR_TOP_PAGE
        memcache.set(CACHE_NAME_FOR_TOP_PAGE_RESULTS,results)
    return render_to_response('mainapp/index.html', {'results': results})

def show_each_page(request,key_name):
    '''
    each page
    '''
    page = AdminPage.get_by_key_name(key_name)
    if page is None:
        return render_to_response('mainapp/404.html', {})
    return render_to_response('mainapp/show_each_page.html', {'page': page})

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

def site_map(request):
    #TODO return sitemap xml for search engine crawler
    return Response('Under construction')
