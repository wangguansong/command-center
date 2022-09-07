from django.contrib import admin
from django.utils.html import format_html
from .models import Location, Tag, Photo, TagRelation, Directory

# Register your models here.

admin.site.register(Location)
admin.site.register(Directory)

class TagRelationInline(admin.TabularInline):
    model = TagRelation
    fk_name = 'collection_tag'
@admin.register(Tag)
class TagAdmin(admin.ModelAdmin):
    list_display = ('tag', 'tag_type', 'title_en')
    list_filter = ('tag_type',)
    inlines = [TagRelationInline]

@admin.register(Photo)
class PhotoAdmin(admin.ModelAdmin):
    list_display = ['thumb_image', 'taken_at', 'location', 'title_en', 'title_zh']
    list_filter = ['directory__dir_path', 'taken_at', ]
    filter_horizontal = ['tags']
    readonly_fields = ['file_name', 'thumb_image']
    fieldsets = (
        (None, {
            'fields': ('thumb_image', 'file_name', 'taken_at', 'location')
        }),
        ('Information', {
            'fields': ('title_en', 'title_zh', 'desc_en', 'desc_zh')
        }),
        ('Tags', {
            'fields': ('favorite', 'hidden', 'tags')
        })
    )
    def thumb_image(self, obj):
        return format_html("<img src='{}' />".format(obj.get_thumb()))
