from django.db import models
import os, re
from PIL import Image
from PIL.ExifTags import TAGS
from django.utils import timezone

OSS_PATH = 'https://images.guansong.wang/'
OSS_LOCAL_DIR = '/home/butters/Photos/'
THUMB_SUFFIX = 'small'
LARGE_SUFFIX = 'original'
PREVIEW_SUFFIX = 'medium'

# Create your models here.

class Location(models.Model):
    location = models.CharField(max_length=128, unique=True)
    country_code = models.CharField(max_length=2)
    title_en = models.CharField(max_length=128)
    title_zh = models.CharField(max_length=128)
    desc_en = models.TextField(blank=True)
    desc_zh = models.TextField(blank=True)
    latitude = models.DecimalField(max_digits=10, decimal_places=8,
                                   blank=True, null=True)
    longitude = models.DecimalField(max_digits=11, decimal_places=8,
                                     blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.location

class Directory(models.Model):
    dir_path = models.CharField(max_length=128, unique=True)
    first_path = models.CharField(max_length=16)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-dir_path',]
        verbose_name_plural = 'directories'

    def __str__(self):
        return self.dir_path
    def get_local_path(self):
        return os.path.join(OSS_LOCAL_DIR, self.first_path, self.dir_path)
    def get_oss_file(self, increment=False):
        file_set = set()
        for (base_dir, _, file_list) in os.walk(self.get_local_path()):
            for file_name in file_list:
                if file_name.lower().endswith(('jpg', 'png', 'jpeg')):
                    file_set.add(os.path.relpath(
                        os.path.join(base_dir, file_name), OSS_LOCAL_DIR))
        if increment:
            db_file_set = set([ photo.file_name for photo in self.photo_set.all() ])
            file_set = file_set - db_file_set
        return file_set
    def add_new_files(self, init_location=None, init_tags=None):
        new_files = self.get_oss_file(increment=True)
        for file_name in new_files:
            new_image = Photo(file_name = file_name,
                              directory = self)
            new_image.taken_at = new_image.guess_datetime()
            new_image.hidden = True if 'Private/' in file_name else False
            if init_location: new_image.location = init_location
            if init_tags: new_image.tags = init_tags
            new_image.save()

        return 
    
class Tag(models.Model):
    TAG_TYPE_CHOICES = (
        (1, 'Normal'),
        (2, 'Collection'),
        (3, 'Name'),
        (4, 'POI'),
    )
    tag = models.CharField(max_length=128, unique=True)
    tag_type = models.SmallIntegerField(choices=TAG_TYPE_CHOICES, default=0)
    title_en = models.CharField(max_length=128)
    title_zh = models.CharField(max_length=128)
    desc_en = models.TextField(blank=True)
    desc_zh = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    components = models.ManyToManyField(
        'self',
        through='TagRelation',
        through_fields=('collection_tag', 'component_tag')
    )

    def __str__(self):
        return self.tag

class TagRelation(models.Model):
    class Meta:
        db_table = 'gallery_tag_relation'
    collection_tag = models.ForeignKey(Tag, on_delete=models.CASCADE,
                                       related_name='collection_tag')
    component_tag = models.ForeignKey(Tag, on_delete=models.CASCADE,
                                      related_name='component_tag')
    created_at = models.DateTimeField(auto_now_add=True)

class Photo(models.Model):
    directory = models.ForeignKey(Directory, on_delete=models.CASCADE)
    file_name = models.CharField(max_length=128, unique=True)
    taken_at = models.DateTimeField(null=True, blank=True)
    location = models.ForeignKey(Location, on_delete=models.CASCADE, blank=True, null=True)
    title_en = models.CharField(max_length=128, blank=True)
    title_zh = models.CharField(max_length=128, blank=True)
    desc_en = models.TextField(blank=True)
    desc_zh = models.TextField(blank=True)
    favorite = models.BooleanField(default=False)
    hidden = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    tags = models.ManyToManyField(Tag)

    class Meta:
        ordering = ['-taken_at',]

    def __str__(self):
        return self.file_name
    def get_thumb(self):
        return OSS_PATH + self.file_name + '!' + THUMB_SUFFIX
    def get_preview(self):
        return OSS_PATH + self.file_name + '!' + PREVIEW_SUFFIX
    def get_original(self):
        return OSS_PATH + self.file_name + '!' + LARGE_SUFFIX
    # SHOULD USE os.path.join BUT file_name IS ABSOLULTE PATH
    def get_local_path(self):
        return os.path.join(OSS_LOCAL_DIR, self.file_name)
    def get_exif(self):
        image_file_path = self.get_local_path()
        exif_table = {}
        image = Image.open(image_file_path)
        info = image.getexif()
        for tag, value in info.items():
            decoded = TAGS.get(tag, tag)
            exif_table[decoded] = value
        return exif_table
    def guess_datetime(self):
        if 'DateTime' in self.get_exif():
            exif_datetime = timezone.make_aware(
                timezone.datetime.strptime(
                    self.get_exif()['DateTime'],
                    '%Y:%m:%d %H:%M:%S'
            ))
            return exif_datetime
        
        # IMG_20220525_071800.jpg
        datetime_re = re.search('(19|20)\d{2}\d{4}_\d{6}',
                                os.path.basename(self.file_name))
        if datetime_re:
            exif_datetime = timezone.make_aware(
                timezone.datetime.strptime(
                    datetime_re.group(),
                    '%Y:%m:%d_%H:%M:%S'
            ))
            return exif_datetime
        
        # mmexport1653230143700.jpg
        timestamp_re = re.search('\d{13}', os.path.basename(self.file_name))
        if timestamp_re:
            exif_datetime = timezone.make_aware(
                timezone.datetime.fromtimestamp(
                    float(timestamp_re.group()) / 1000
            ))
            return exif_datetime

        return