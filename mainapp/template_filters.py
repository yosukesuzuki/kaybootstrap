# -*- coding: utf-8 -*-

'''
original template filters by kaybootstrap
'''
def toMarkdown(text):
    import markdown
    return_html = markdown.markdown(text) 
    return return_html
