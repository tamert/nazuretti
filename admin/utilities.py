from .imports import *

def photo_formatter(self, model, name):
  if name is 'photo' and model.photo:
    url = url_for('static', filename='uploads/' + model.photo) + '?' + str(random.random())
    return wtf.HTMLString(u'<img src="%s" height="40" />' % url)
  elif name is 'photo':
    return wtf.HTMLString(u'')

