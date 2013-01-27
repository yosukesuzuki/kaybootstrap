# -*- coding: utf-8 -*-

'''
original template filters by kaybootstrap
'''
import datetime

def toMarkdown(text):
    from mainapp.markdown2 import markdown
    return_html = markdown(text) 
    return return_html

def enforceMinus9hours(datetime_string):
    display_time = datetime.datetime.strptime(datetime_string,'%Y-%m-%d %H:%M')
    display_time = display_time + datetime.timedelta(hours = -9)
    return_datetime_string = display_time.strftime('%Y-%m-%d %H:%M')
    return return_datetime_string
    
