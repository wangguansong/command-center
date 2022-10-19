from django.contrib import admin, messages
from django.http import HttpResponseRedirect
from django.utils.html import format_html
from django.utils.translation import ngettext
from django.shortcuts import render
from django import forms
from .models import Location, Tag, Photo, TagRelation, Directory
from .handler import get_oss_directories

# Register your models here.

admin.site.register(Location)


@admin.register(Directory)
class DirectoryAdmin(admin.ModelAdmin):
    actions = [
        'scan_directories',
    ]

# https://www.willandskill.se/en/articles/custom-django-admin-actions-with-an-intermediate-page
    @admin.action(description='Scan for New Directories')
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
    list_filter = ['taken_at', 'hidden', 'directory__dir_path', ]
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

    actions = [
        'set_location',
        'add_tags',
        'remove_tags',
    ]

    @admin.action(description='Set Location')
    def set_location(self, request, queryset):

        class PhotoSetLocationForm(forms.ModelForm):
            class Meta:
                model = Photo
                fields = ['location']

        form = PhotoSetLocationForm()

        if 'location' in request.POST:
            location_id = int(request.POST.get('location'))
            if (location_id > 0):
                queryset.update(location=location_id)

            self.message_user(
                request,
                'Successfully changed location of * photos to xxx.',
                messages.SUCCESS,
            )
            return HttpResponseRedirect(request.get_full_path())
        else:
            form = PhotoSetLocationForm()
        #app_label = opts.app_label

        context = {
            **self.admin_site.each_context(request),
            "title": 'Set Photo Location',
            "subtitle": None,
            "photos": queryset,
            "media": self.media,
            "opts": self.model._meta,
            "form": form,
        }
        return render(request,
                      'admin/photo_set_location.html',
                      context=context)


    @admin.action(description='Add Tags')
    def add_tags(self, request, queryset):
        class PhotoAddTagsForm(forms.ModelForm):
            class Meta:
                model = Photo
                fields = ['tags']

        if 'tags' in request.POST:
            selected_tags = request.POST.getlist('tags')
            for photo in queryset:
                photo.tags.add(*selected_tags)

            self.message_user(
                request,
                'Successfully added * tags to * photos.',
                messages.SUCCESS,
            )

            return HttpResponseRedirect(request.get_full_path())
        else:
            form = PhotoAddTagsForm()
 
        context = {
            **self.admin_site.each_context(request),
            "title": 'Add Common Tags',
            "subtitle": None,
            "photos": queryset,
            "opts": self.model._meta,
            "form": form,
        }
        return render(request,
                      'admin/photo_add_tags.html',
                      context=context)

    @admin.action(description='Remove Tags')
    def remove_tags(self, request, queryset):
        pass
