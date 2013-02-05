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
import datetime
import time

from google.appengine.api.images import get_serving_url

from mainapp.models import AdminPage,BlobStoreImage,Article

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


