import random

import os
import flask

from flask import request, url_for
from flask.ext.wtf import FileField, widgets
from wtforms.widgets import core as wtf
from werkzeug import secure_filename 

app = flask.current_app

class ImageUploadWidget(widgets.FileInput):
  def __init__(self, upload_options={}):
    super(ImageUploadWidget, self).__init__()
    self.upload_base_url = upload_options.get('base_url', app.config.get('UPLOAD_BASE_URL', ''))
    self.max_width       = upload_options.get('max_width', None)
    self.mirror_url      = upload_options.get('mirror_url', app.config.get('UPLOAD_MIRROR_URL', None))
    self.crop            = upload_options.get('crop', None)
    self.resize          = upload_options.get('resize', None)
    self.thumbnails      = upload_options.get('thumbnails', [])
    self.show_current    = upload_options.get('show_current', True)
    self.model_name      = upload_options.get('model', None)

  def __call__(self, field, **kwargs):
    if self.max_width:
      kwargs['data-max-width']  = self.max_width

    if self.mirror_url:
      kwargs['data-url'] = self.mirror_url

    if self.model_name:
      kwargs['data-model-name'] = self.model_name
      self.upload_base_url += self.model_name + '/'
      
    if self.crop:
      if self.crop.__class__ == dict:
        kwargs['data-crop'] = 'true'
        for key, value in self.crop.iteritems():
          if value.__class__ == tuple:
            (width, height) = value
            kwargs['data-crop-%s-width' % key] = str(width)
            kwargs['data-crop-%s-height' % key] = str(height)
          else:
            kwargs['data-crop-%s' % key] = str(value)

    html = ''
    if field.data and field.data != '':
      if self.show_current:
        current_image_params = dict(
          src = url_for('static', filename=self.upload_base_url + field.data) + '?' + str(random.random()),
        )

        if self.max_width:
          current_image_params['style'] = current_image_params.get('style', '') + 'width: %spx;' % self.max_width

        html += wtf.HTMLString(u'<strong>%s</strong>' % 'Suanki Resim:')
        html += wtf.HTMLString(u'<div><img %s /></div>' % wtf.html_params(**current_image_params))

      params = dict(
        name  = '%s-old' % (field.name),
        value = field.data,
        type  = 'hidden'
      )
      html += wtf.HTMLString(u'<input %s>' % wtf.html_params(**params))

    html += super(ImageUploadWidget, self).__call__(field, **kwargs)

    if self.resize:
      if self.resize.__class__ == tuple:
        (width, height) = self.resize
        width_params = dict(type="hidden", name="%s-resize-width" % field.name, value=width)
        height_params = dict(type="hidden", name="%s-resize-height" % field.name, value=height)
        html += wtf.HTMLString(u'<input %s>' % wtf.html_params(**width_params))
        html += wtf.HTMLString(u'<input %s>' % wtf.html_params(**height_params))

    for i, thumb in enumerate(self.thumbnails):
      (width, height) = thumb['size']
      name_params   = dict(type="hidden", name="%s-thumbnail[%d][name]" % (field.name, i), value=thumb['name'])
      width_params = dict(type="hidden", name="%s-thumbnail[%d][width]" % (field.name, i), value=width)
      height_params = dict(type="hidden", name="%s-thumbnail[%d][height]" % (field.name, i), valu=height)

      html += wtf.HTMLString(u'<input %s>' % wtf.html_params(**name_params))
      html += wtf.HTMLString(u'<input %s>' % wtf.html_params(**width_params))
      html += wtf.HTMLString(u'<input %s>' % wtf.html_params(**height_params))

    return html

class ImageUploadField(FileField):
  def __init__(self, label='', validators=None, upload_options={}, **kwargs):
    self.widget = ImageUploadWidget(upload_options=upload_options)
    super(ImageUploadField, self).__init__(label, validators, **kwargs)
    
  def _value(self):
    if self.data:
      return secure_filename(self.data)
    else:
      return u''

  def post_validate(self, form, changed):
    if self.data:
      self.data = secure_filename(self.data.filename)
    elif request.form.has_key(self.name + '-old'):
      self.data = request.form[self.name + '-old']
    else:
      self.data = None
