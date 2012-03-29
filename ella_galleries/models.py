from django.db import models
from django.utils.translation import ugettext_lazy as _
from django.utils.datastructures import SortedDict

from ella.core.models import Publishable
from ella.core.cache import cache_this, CachedForeignKey
from ella.core.custom_urls import resolver
from ella.photos.models import Photo


def get_gallery_key(gallery):
    return 'galitems:%d' % gallery.id

class Gallery(Publishable):
    """
    Represents a Gallery of ``Photo`` objects.
    
    ``content`` use used to keep gallery description when rendering.
    """
    content = models.TextField(_('Content'), blank=True)
    created = models.DateTimeField(_('Created'), auto_now_add=True)

    class Meta:
        verbose_name = _('Gallery')
        verbose_name_plural = _('Galleries')

    @property
    def items(self):
        """
        Returns sorted dict of gallery items. Unique items slugs are used as keys.
        """
        if self.id:
            if not hasattr(self, '_items'):
                self._items = self._get_gallery_items()
            return self._items
        return SortedDict()

    @cache_this(get_gallery_key)
    def _get_gallery_items(self):
        slugs_count = {}
        itms = [(item, item.photo) for item in self.galleryitem_set.all()]
        slugs_unique = set((i[1].slug for i in itms))
        res = SortedDict()

        for item, target in itms:
            # poor man's identity mapper
            item.gallery = self
            slug = target.slug
            if slug not in slugs_count:
                slugs_count[slug] = 1
                res[slug] = item
            else:
                while "%s%s" % (slug, slugs_count[slug]) in slugs_unique:
                    slugs_count[slug] += 1
                new_slug = "%s%s" % (slug, slugs_count[slug])
                slugs_unique.add(new_slug)
                res[new_slug] = item
        return res

    def get_photo(self):
        if self.photo_id:
            return self.photo

        it = self.items
        if it:
            return it.values()[0].photo

        return None


class GalleryItem(models.Model):
    """
    One photo in a ``Gallery``. ``GalleryItem`` adds specific metadata for 
    membership in gallery such as:
    
    ``order`` - position of photo in the gallery
    ``title`` - specific title in the gallery, can be blank
    ``text`` - description of photo in the gallery, can be blank too
    """
    gallery = models.ForeignKey(Gallery, verbose_name=_("Parent gallery"))
    photo = CachedForeignKey(Photo, verbose_name=_("Photo"))
    order = models.IntegerField(_('Object order'))

    title = models.CharField(_('Title'), max_length=255, blank=True)
    text = models.TextField(blank=True)

    class Meta:
        ordering = ('order',)
        verbose_name = _('Gallery item')
        verbose_name_plural = _('Gallery items')


    def __unicode__(self):
        return u"%s %s %s" % (self.photo, _('in gallery'), self.gallery.title)

    def __get_slug(self):
        for slug, item in self.gallery.items.items():
            if item == self:
                return slug

    def get_slug(self):
        """
        Return a unique slug for given gallery, even if there are more objects
        with the same slug.
        """
        if not hasattr(self, '__slug'):
            self.__slug = self.__get_slug()
        return self.__slug

    def get_absolute_url(self):
        if self.order == 0:
            return self.gallery.get_absolute_url()
        return resolver.reverse(self.gallery, 'gallery-item-detail', self.get_slug())


