from django.contrib import admin
from django.utils.html import format_html
from django.shortcuts import render
from .models import Location, Tag, Photo, TagRelation, Directory
from .handler import get_oss_directories

# Register your models here.

admin.site.register(Location)


@admin.register(Directory)
class DirectoryAdmin(admin.ModelAdmin):
    actions = ['scan_directories']

# https://www.willandskill.se/en/articles/custom-django-admin-actions-with-an-intermediate-page
    @admin.action(description='Scan for new Directories')
    def scan_directories(self, request, queryset):
        full_list = get_oss_directories()
        db_list = set([ (dir.first_path, dir.dir_path)
                        for dir in Directory.objects.all() ])
        new_list = full_list - db_list
        context = {
            **self.admin_site.each_context(request),
            "title": 'test title',
            "subtitle": None,
            "queryset": queryset,
            "media": self.media,
            "new_list": new_list,
        }
        return render(request,
                      'admin/scan_new_directories.html',
                      context=context)


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
    date_hierarchy = 'taken_at'
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
