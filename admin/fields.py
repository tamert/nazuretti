from .imports import *

class FileUploadWidget(widgets.FileInput):
  def __call__(self, field, **kwargs):
    kwargs['data-url'] = '/admin/mirrorimage/'

    cropper_params = dict(
      id = '%s-cropper' % (field.name),
    )

    html = ''
    if field.data and field.data != '':
      params = dict(
        name  = '%s-old' % (field.name),
        value = field.data,
        type  = 'hidden'
      )

      current_image_params = dict(
        src = url_for('static', filename='uploads/' + field.data) + '?' + str(random.random()),
        style = 'max-width: 400px;'
      )

      html += wtf.HTMLString(u'<strong>%s</strong>' % 'Suanki Resim:')
      html += wtf.HTMLString(u'<div><img %s /></div>' % wtf.html_params(**current_image_params))
      html += wtf.HTMLString(u'<input %s>' % wtf.html_params(**params))

    html += super(FileUploadWidget, self).__call__(field, **kwargs)
    html += wtf.HTMLString(u'<div %s></div>' % wtf.html_params(**cropper_params))

    return html

class FileUploadField(FileField):
  widget = FileUploadWidget()
  def _value(self):
    if self.data:
      return secure_filename(self.data)
    else:
      return u''
