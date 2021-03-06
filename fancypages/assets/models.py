from django.db import models
from django.utils.translation import ugettext as _

from ..compat import get_user_model

User = get_user_model()


class AbstractAsset(models.Model):
    name = models.CharField(_("Name"), max_length=255)

    date_created = models.DateTimeField(_("Date created"), auto_now_add=True)
    date_modified = models.DateTimeField(_("Date modified"), auto_now=True)

    description = models.TextField(_("Description"), default="")
    creator = models.ForeignKey(User, verbose_name=_("Creator"))

    def __unicode__(self):
        return self.name

    class Meta:
        abstract = True


class ImageAsset(AbstractAsset):
    image = models.ImageField(
        upload_to='asset/images/%Y/%m',
        width_field='width',
        height_field='height',
        verbose_name=_("Image")
    )
    width = models.IntegerField(_("Width"), blank=True)
    height = models.IntegerField(_("Height"), blank=True)
    size = models.IntegerField(_("Size"), blank=True, null=True)  # Bytes

    @property
    def asset_type(self):
        return self._meta.object_name.lower()

    def get_absolute_url(self):
        return self.image.url
