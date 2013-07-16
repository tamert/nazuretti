#-*- encoding: utf-8-*-
from .fields import ImageUploadField

def process_image_uploads(form, model, **kwargs):
  for field in form:
    if field.__class__ == ImageUploadField:
      import pudb
      pudb.set_trace()
