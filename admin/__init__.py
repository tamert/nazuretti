#-*-encoding: utf-8-*-
from .imports import *

#from . import orders
from . import product
from . import mirror
from . import pictures
from . import news
from . import site_settings

images = UploadSet('imagse', IMAGES, default_dest=lambda x: flask.current_app.config['UPLOAD_FOLDER'])
configure_uploads(flask.current_app, (images,))

admin = Admin(flask.current_app, name=u'Yönetim Paneli', index_view=site_settings.IndexView(name='Anasayfa'))
#admin.add_view(ModelView(models.Page, models.db.session))
admin.add_view(product.ProductView(models.db.session, name=u'Ürünler'))
admin.add_view(pictures.PictureView(models.db.session, name=u'Fotoğraflar'))
admin.add_view(news.NewsView(models.db.session, name=u'Haberler'))
admin.add_view(site_settings.SiteSettingsView(name=u'Genel Ayarlar'))
admin.add_view(mirror.MirrorImage())
