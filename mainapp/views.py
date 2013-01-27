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
import json
import datetime
from werkzeug import Response

from google.appengine.api import files
from google.appengine.api import memcache

from django.utils import html

from kay.utils import render_to_response
from kay.utils import get_by_key_name_or_404
from kay.utils import url_for 
from kay.utils.paginator import Paginator, InvalidPage, EmptyPage
from kay.i18n import gettext as _
from kay.auth.decorators import admin_required
from settings import DEFAULT_LANG

from mainapp.markdown2 import markdown
from mainapp.models import AdminPage,BlobStoreImage,Article

'''
global vars
'''
TOP_PAGE_CONTENT_NUM = 4
CACHE_NAME_FOR_TOP_PAGE_RESULTS = 'top-page-contents'
DUMMY_DATA_FOR_TOP_PAGE = [{'title':'Dummy,first title','snippet':'this is dummy snippet','url':'/first/'},
        {'title':'Dummy,second title','snippet':'this is dummy snippet','url':'/second/'},
        {'title':'Dummy,third title','snippet':'this is dummy snippet','url':'/third/'},
        {'title':'Dummy,fourth title','snippet':'this is dummy snippet','url':'/fourth/'}]
MODEL_DICT = {'AdminPage':AdminPage,'BlobStoreImage':BlobStoreImage,'Article':Article}

def index(request):
    '''
    top page
    '''
    browser_lang = request.lang
    results = memcache.get(CACHE_NAME_FOR_TOP_PAGE_RESULTS+'-'+browser_lang)
    if results is None:
        query_results = AdminPage.all().filter(u'lang =',DEFAULT_LANG).filter(u'display_page_flg =',True).order('page_order').fetch(limit=TOP_PAGE_CONTENT_NUM)
        results = []
        for r in query_results:
            if browser_lang != DEFAULT_LANG:
                translations = AdminPage.all().ancestor(r.key()).fetch(1000)
                browser_lang_trans = None
                for trans in translations:
                    if trans.lang == browser_lang:
                        browser_lang_trans = trans
                        break
                if browser_lang_trans:
                    r.content = browser_lang_trans.content
                    r.title = browser_lang_trans.title
            url = r.external_url if r.external_url else '/'+r.key().name()+'/'
            snippet = html.strip_tags(markdown(r.content)).split('\n')[0]
            try:
                first_image = json.loads(r.images)['images'][0]['image_path']
            except:
                first_image = None
            results.append({'title':r.title,'snippet':snippet,'url':url,'first_image':first_image})
        if len(results) == 0:results = DUMMY_DATA_FOR_TOP_PAGE
        logging.info(results)
        memcache.set(CACHE_NAME_FOR_TOP_PAGE_RESULTS+'-'+browser_lang,results)
    return render_to_response('mainapp/index.html', {'results': results})

def show_each_page(request,key_name):
    '''
    each page
    '''
    browser_lang = request.lang
    model_name = 'AdminPage'
    page = get_page_content(browser_lang,model_name,key_name)
    if page is None:
        return render_to_response('mainapp/404.html', {})
    sidebar = {'sidebar_title':_('Link'),'sidebar_list':[{'title':_('About'),'url':'/about/'},{'title':_('Contact'),'url':'/contact/'}]}
    return render_to_response('mainapp/show_each_page.html', {'page': page,'model_name':model_name,'sidebar':sidebar})

def get_page_content(browser_lang,model_name,key_name):
    page = MODEL_DICT[model_name].get_by_key_name(key_name)
    if browser_lang != DEFAULT_LANG:
        logging.info('browser_lang:'+browser_lang)
        translations = MODEL_DICT[model_name].all().ancestor(page.key()).fetch(1000)
        for trans in translations:
            if trans.lang == browser_lang:
                page = trans 
    return page

def article_list(request):
    browser_lang = request.lang
    article_per_page = 10
    try:
        page = int(request.args.get('page','1'))
    except ValueError:
        page = 1
    results_dic = get_article_list(browser_lang,page,article_per_page)
    return render_to_response('mainapp/article_list.html', {'article_results':results_dic})

def show_each_article(request,key_name):
    browser_lang = request.lang
    model_name = 'Article'
    page = get_page_content(browser_lang,model_name,key_name)
    if page is None:
        return render_to_response('mainapp/404.html', {})
    results_dic = get_article_list(browser_lang,1,10)
    sidebar = {'sidebar_title':_('Back number'),'sidebar_list':results_dic['articles']}
    return render_to_response('mainapp/show_each_page.html', {'page': page,'model_name':model_name,'sidebar':sidebar})

def get_article_list(browser_lang,page,article_per_page):
    memcache_key = 'article-'+str(page)+'-'+str(article_per_page)+'-'+browser_lang
    logging.info(memcache_key)
    results_dic = memcache.get(memcache_key)
    if results_dic is None:
        now = datetime.datetime.now()
        logging.info(now)
        query = Article.all().filter(u'lang =',DEFAULT_LANG).filter(u'display_page_flg =',True).filter(u'display_time <',now).order('-display_time')
        paginator = Paginator(query,article_per_page)
        try:
            results = paginator.page(page)
        except (EmptyPage,InvalidPage):
            results = paginator.page(paginator.num_pages)
        return_list = []
        for r in results.object_list:
            if browser_lang != DEFAULT_LANG:
                translations = Article.all().ancestor(r.key()).fetch(1000)
                browser_lang_trans = None
                for trans in translations:
                    if trans.lang == browser_lang:
                        browser_lang_trans = trans
                        break
                if browser_lang_trans:
                    r.content = browser_lang_trans.content
                    r.title = browser_lang_trans.title
            url = r.external_url if r.external_url else url_for('mainapp/show_each_article',key_name=r.key().name())
            snippet = html.strip_tags(markdown(r.content)).split('\n')[0]
            try:
                first_image = json.loads(r.images)['images'][0]['image_path']
            except:
                first_image = None
            return_list.append({'key':str(r.key()),
                'id':r.key().name(),
                'title':r.title,
                'snippet':snippet,
                'url':url,
                'first_image':first_image,
                'display_time':str(r.display_time)[:16]})
        results_dic = {'articles':return_list,
        'current_page':results.number,
        'total_pages':results.paginator.num_pages}
        memcache.set(memcache_key,results_dic)
    return results_dic 
 
def site_map(request):
    #TODO return sitemap xml for search engine crawler
    return Response('Under construction')
