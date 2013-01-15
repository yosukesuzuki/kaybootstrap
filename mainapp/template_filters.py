# -*- coding: utf-8 -*-

'''
original template filters by kaybootstrap
'''
def toMarkdown(text):
    from mainapp.markdown2 import markdown
    return_html = markdown(text) 
    return return_html
