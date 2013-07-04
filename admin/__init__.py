from .imports import *

from . import orders
from . import product
from . import mirror

images = UploadSet('imagse', IMAGES, default_dest=lambda x: flask.current_app.config['UPLOAD_FOLDER'])
configure_uploads(flask.current_app, (images,))

admin = Admin(flask.current_app)
admin.add_view(ModelView(models.Page, models.db.session))
admin.add_view(product.ProductView(models.db.session))
admin.add_view(mirror.MirrorImage())
