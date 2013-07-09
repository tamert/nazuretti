import Image as I

class Image():
  def __init__(self, path):
    self.path  = path
    self.image = I.open(path)

    self.width, self.height = self.image.size
    self.is_wider = self.width > self.height


  def crop(self, box):
    self.image = self.image.crop(box)


  def thumbnail(self, size):
    width, height = size

    if self.is_wider:
      self.image.thumbnail((100000, height), I.ANTIALIAS)
      self.width, self.height = self.image.size

      diff_w = width - self.width
      diff_h = 0

    else:
      self.image.thumbnail((width, 100000), I.ANTIALIAS)
      self.width, self.height = self.image.size

      diff_w = 0
      diff_h = height - self.height

    box = (diff_w, diff_h, diff_w + width, diff_h + height)
    self.image = self.image.crop(box)


  def resize(self, size):
    self.image.thumbnail(size, I.ANTIALIAS)

  
  def save(self, path, keep_old=True):
    self.image.save(path, quality=100)

    if not keep_old and isfile(self.path):
      os.remove(self.path)
      self.path = path

