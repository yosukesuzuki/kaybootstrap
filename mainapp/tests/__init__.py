# -*- coding: utf-8 -*-


import datetime
import json
from kay.ext.testutils.gae_test_base import GAETestBase

from mainapp.models import Article,AdminPage
from mainapp.views import get_page_content,get_search_list
from adminapp.views import index_full_text_search,index_full_text_search_by_key_name

class GetArticleTest(GAETestBase):

    CLEANUP_USED_KIND = True
    USE_PRODUCTION_STUBS = True

    def test_get_article(self):
        images = {'images': [{'title': '', 'image_path': '//0.0.0.0:8080/_ah/img/WIW0aePJFuNVe9x13v9rIg==', 'id': '668cf791e9e9e7f70669f4931567e3d9'}]}
        tags = ['hoge1','hoge2']
        test_data = {'key_name':'hoge','display_page_flg':True,'display_time':datetime.datetime.now(),
                'title':'hoge_title','url':'hoge_url','content':'hogehohoge\nhogehogeho\nhogehoge',
                'tags_string':','.join(tags),'tags':tags,'images':images,'lang':'en'}
        entity1 = Article(key_name=test_data['key_name'],display_page_flg=test_data['display_page_flg'],display_time=test_data['display_time'],
                title=test_data['title'],url=test_data['url'],content=test_data['content'],
                tags_string=test_data['tags_string'],tags=test_data['tags'],images=json.dumps(test_data['images']),lang=test_data['lang'])
        entity1.put()
        result = get_page_content('en','Article','hoge')
        self.assertEquals(result.title,'hoge_title')
