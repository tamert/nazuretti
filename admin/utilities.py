from .imports import *

def photo_formatter(self, model, name):
  if name is 'photo' and model.photo:
    url = url_for('static', filename='uploads/' + model.photo) + '?' + str(random.random())
    return wtf.HTMLString(u'<img src="%s" style="width: 300px;" />' % url)
  elif name is 'photo':
    return wtf.HTMLString(u'')
  elif name is 'image' and model.image:
    url = url_for('static', filename='uploads/pictures/' + model.image) + '?' + str(random.random())
    return wtf.HTMLString(u'<img src="%s" style="width: 300px;" />' % url)
  elif name is 'image':
    return wtf.HTMLString(u'')


