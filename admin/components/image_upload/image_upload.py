#-*- encoding: utf-8-*-
import os
import random
from os.path import isfile, isdir
from flask   import request, current_app, url_for
from flask.ext import wtf 

from .fields import ImageUploadField
from .image  import Image as ImageKit

upload_folder = current_app.config['UPLOAD_FOLDER']

def get_image_column_formatter(field, field_name):
  base_url = 'uploads/'
  upload_options = field.kwargs.get('upload_options', None)
  model_name = upload_options.get('model', None)
  if model_name:
    base_url = 'uploads/' + model_name + '/'

  def formatter(self, model, name):
    if getattr(model, field_name, None):
      url = url_for('static', filename = base_url + getattr(model, field_name)) + '?' + str(random.random())

    return wtf.HTMLString(u'<img src="%s" style="width: 300px;" />' % url)

  return formatter

def remove_files_after_deletion(form, model):
  for field_name in form.__dict__.keys():
    field = getattr(form, field_name)

    if getattr(field, 'field_class', None) == ImageUploadField:
      if getattr(model, field_name):
        field_options = field.kwargs.get('upload_options', {})
        model_name = field_options.get('model', '')
        thumbnails = field_options.get('thumbnails', [])

        file_name = getattr(model, field_name, '')
        file_path = os.path.join(upload_folder, model_name, file_name)
        thumbs_dir = os.path.join(upload_folder, model_name, 'thumbnails')

        if isfile(file_path):
          os.remove(file_path)

        for thumb in thumbnails:
          thumb_file_name = ImageKit.append_name(file_name, thumb['name'])
          thumb_file_path = os.path.join(thumbs_dir, thumb_file_name)

          if isfile(thumb_file_path):
            os.remove(thumb_file_path)

def update_filenames_to_model(form, model, db):
  for field in form:
    if field.__class__ == ImageUploadField:
      if getattr(model, field.name):
        model_name = field.widget.model_name
        new_filename = str(model.id) + '_' + getattr(model, field.name)

        if model_name:
          old_file_path = os.path.join(upload_folder, model_name, getattr(model, field.name))
          new_file_path = os.path.join(upload_folder, model_name, new_filename)
        else:
          old_file_path = os.path.join(upload_folder, getattr(model, field.name))
          new_file_path = os.path.join(upload_folder, new_filename)

        thumbnails = []
        if len(field.widget.thumbnails) > 0:
          for thumbnail in field.widget.thumbnails:
            thumbnail_image_name = ImageKit.append_name(getattr(model, field.name), thumbnail['name'])
            new_thumbnail_image_name = str(model.id) + '_' + ImageKit.append_name(getattr(model, field.name), thumbnail['name'])
            if model_name:
              old_path = os.path.join(upload_folder, model_name, 'thumbnails', thumbnail_image_name)
              new_path = os.path.join(upload_folder, model_name, 'thumbnails', new_thumbnail_image_name)
            else:
              old_path = os.path.join(upload_folder, 'thumbnails', thumbnail_image_name)
              new_path = os.path.join(upload_folder, 'thumbnails', new_thumbnail_image_name)

            thumbnails.append(dict(old_path=old_path, new_path=new_path))

        if isfile(old_file_path):
          os.rename(old_file_path, new_file_path)
          setattr(model, field.name, new_filename)
          db.session.add(model)
          db.session.commit()

        for thumbnail in thumbnails:
          if isfile(thumbnail['old_path']):
            os.rename(thumbnail['old_path'], thumbnail['new_path'])

def process_image_uploads(form, model, db):
  for field in form:
    if field.__class__ == ImageUploadField:
      new_filename  = request.form.get(field.name + '-filename', '')
      crop          = field.widget.crop
      resize        = field.widget.resize
      thumbnails    = field.widget.thumbnails
      model_name    = field.widget.model_name
      upload_folder = current_app.config['UPLOAD_FOLDER']
      old_photo     = request.form.get(field.name + '-old', None)
      old_photo_path = None

      if model_name:
        mirror_path    = os.path.join(upload_folder, 'mirror', model_name, new_filename)
        new_path       = os.path.join(upload_folder, model_name, new_filename)
        thumbs_dir     = os.path.join(upload_folder, model_name, 'thumbnails')
        images_dir     = os.path.join(upload_folder, model_name)

        if old_photo:
          old_photo_path = os.path.join(upload_folder, model_name, old_photo)
      else:
        mirror_path    = os.path.join(upload_folder, 'mirror', new_filename)
        new_path       = os.path.join(upload_folder, new_filename)
        thumbs_dir     = os.path.join(upload_folder, 'thumbnails')
        images_dir     = upload_folder

        if old_photo:
          old_photo_path = os.path.join(upload_folder, old_photo)

      if not isdir(images_dir):
        os.mkdir(images_dir)

      if new_filename == '':
        setattr(model, field.name, old_photo)
        db.session.add(model)
        db.session.commit()

      else:
        img = ImageKit(mirror_path)
        if crop:
          box = (
            int(float(request.form.get(field.name + '-x', '0'))),
            int(float(request.form.get(field.name + '-y', '0'))),
            int(float(request.form.get(field.name + '-x2', '0'))),
            int(float(request.form.get(field.name + '-y2' , '0')))
          )
          img.crop(box)

        if resize:
          img.resize(resize)

        img.save(new_path)

        if len(thumbnails) > 0:
          for thumbnail in thumbnails:
            img = ImageKit(new_path)
            thumbnail_path = os.path.join(thumbs_dir, ImageKit.append_name(new_filename, thumbnail['name']))

            if not isdir(thumbs_dir):
              os.mkdir(thumbs_dir)

            img.thumbnail(thumbnail['size'])
            img.save(thumbnail_path)

        setattr(model, field.name, new_filename)
        db.session.add(model)
        db.session.commit()

        if isfile(mirror_path):
          os.remove(mirror_path)

        if model and hasattr(model, 'id') and model.id > 0:
          if old_photo and old_photo != new_filename:
            if isfile(old_photo_path):
              os.remove(old_photo_path)
