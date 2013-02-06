import ella_newman as newman

from django.utils.translation import ugettext_lazy as _
from django.forms import models as modelforms

from ella.core.newman_admin import ListingInlineAdmin, PublishableAdmin

from ella_galleries.models import Gallery, GalleryItem

class GalleryItemForm(modelforms.ModelForm):
    def reset_errors(self):
        self._errors = None

    def full_clean(self):
        " little hack to prevent errors when empty photo ID is filled in "
        ini_key = 'target_id'
        key = '%s-%s' % (self.prefix, ini_key)
        self.reset_errors()
        if key in self.data and self.initial.get(ini_key, False):
            if not self.data[key]:
                self.data._mutable = True
                self.data[key] = u'%d' % self.initial[ini_key]
                self.data._mutable = False
        super(GalleryItemForm, self).full_clean()


class GalleryItemInline(newman.options.NewmanInlineModelAdmin):
    template = 'newman/edit_inline/gallery_item.html'
    model = GalleryItem
    extra = 1
    form = GalleryItemForm
    raw_id_fields = ('photo',)
    verbose_name = _('Photos')


class GalleryAdmin(PublishableAdmin):
    ordering = ('-created',)
    fieldsets = (
        (_("Heading"), {'fields': ('title', 'slug',)}),
        (_("Metadata"), {'fields': ('photo', 'category', 'authors', 'source')}),
        (_("Content"), {'fields': ('description', 'content',)}),
    )
    list_filter = ('created', 'category',)
    search_fields = ('title', 'description', 'slug',)
    inlines = [GalleryItemInline, ListingInlineAdmin]
    rich_text_fields = {'small': ('description',), None: ('content',)}
    prepopulated_fields = {'slug': ('title',)}

    def photo_thumbnail(self, object):
        " Assign first of GalleryItems as Gallery.photo if not set. "
        object.assign_photo()
        return super(GalleryAdmin, self).photo_thumbnail(object)
    photo_thumbnail.allow_tags = True
    photo_thumbnail.short_description = _('Photo')

newman.site.register(Gallery, GalleryAdmin)

