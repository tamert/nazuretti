import Image as I

class Image():
  def __init__(self, path):
    self.path  = path
    self.image = I.open(path)

    self.width, self.height = self.image.size
    self.is_wider = self.width > self.height
    self.is_tall  = not self.is_wider


  def crop(self, box):
    self.image = self.image.crop(box)


  def thumbnail(self, size):
    width, height = size
    thumb_is_wider = width > height
    thumb_is_tall  = not thumb_is_wider

    if self.is_tall and thumb_is_tall:
      self.image.thumbnail((width, 100000), I.ANTIALIAS)
      self.width, self.height = self.image.size
      top = (self.height / 2) - (height / 2)
      box = (0, top, width, top + height)


    elif self.is_tall and thumb_is_wider:
      self.image.thumbnail((width, 100000), I.ANTIALIAS)
      self.width, self.height = self.image.size
      top = (self.height / 2) - (height / 2)
      box = (0, top, width, top + height)

    elif self.is_wider and thumb_is_tall:
      self.image.thumbnail((100000, height), I.ANTIALIAS)
      self.width, self.height = self.image.size
      left = (self.width / 2) - (width / 2)
      box = (left, 0, left + width, height)

    self.image = self.image.crop(box)

  def resize(self, size):
    self.image.thumbnail(size, I.ANTIALIAS)

  def save(self, path, keep_old=True):
    self.image.save(path, quality=100)

    if not keep_old and isfile(self.path):
      os.remove(self.path)
      self.path = path

  @staticmethod
  def append_name(base_name, appendix):
    filename_parts = base_name.split('.')
    filename = ".".join(filename_parts[:-1])
    file_ext = filename_parts[-1]

    return '%s-%s.%s' % (filename, appendix, file_ext)
