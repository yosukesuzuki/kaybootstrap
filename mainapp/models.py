# -*- coding: utf-8 -*-
# mainapp.models

from google.appengine.ext import db
from google.appengine.ext import blobstore
from google.appengine.api import images
from kay.auth.models import GoogleUser
# Create your models here.

class AdminTopPage(db.Model):
    '''
    Model for top page setting.
    If admin set Url field, url is set as key name or escaped Title String is set as key name
    '''
    title = db.StringProperty(verbose_name='Title',required=True)
    display_page_flg = db.BooleanProperty(verbose_name=u'Display a page or hidden',default=False)
    page_order = db.IntegerProperty(verbose_name=u'Page order on top page',default=99999)
    snippet = db.TextProperty(verbose_name='Snippet')
    content = db.TextProperty(verbose_name='Content')
    url = db.StringProperty(verbose_name='Url,page identifier of this content,only at first time')
    external_url = db.StringProperty(verbose_name='External Url(If link to an outside page,optional)')
    images = db.TextProperty(verbose_name='Images,JSON Format')
    image_layout = db.StringProperty(verbose_name='Image Layout Setting',choices=('auto','manual'),default='auto')
    show_image_on_top_flg = db.BooleanProperty(verbose_name=u'Show the first image on top page',default=True)
    update = db.DateTimeProperty(auto_now=True)
    created = db.DateTimeProperty(auto_now_add=True)
