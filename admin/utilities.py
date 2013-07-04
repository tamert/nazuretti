from .imports import *

def photo_formatter(self, context, model, name):
  if name is 'photo':
    url = url_for('static', filename='uploads/' + model.photo) + '?' + str(random.random())
    return wtf.HTMLString(u'<img src="%s" height="40" />' % url)

