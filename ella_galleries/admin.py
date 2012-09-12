from django.conf import settings
from django.contrib import admin
from django.utils.translation import ugettext_lazy as _

from ella.core.admin import (PublishableAdmin, ListingInlineAdmin,
                             RelatedInlineAdmin)

from ella_galleries.models import Gallery, GalleryItem


class GalleryItemTabularOptions(admin.TabularInline):
    model = GalleryItem
    extra = getattr(settings, 'ELLA_GALLERIES_ADMIN_EXTRA_INLINES', 10)


class GalleryOptions(PublishableAdmin):
    ordering = ('-publish_from',)
    fieldsets = (
        (_("Gallery heading"), {'fields': ('title', 'slug')}),
        (_("Gallery contents"), {'fields': ('description', 'content')}),
        (_("Metadata"), {
            'fields': ('category', 'authors', 'source', 'photo')
        }),
        (_("Publication"), {
            'fields': (('publish_from', 'publish_to'), 'published', 'static')
        }),
    )
    inlines = [GalleryItemTabularOptions, ListingInlineAdmin,
               RelatedInlineAdmin]

admin.site.register(Gallery, GalleryOptions)
