from django.db import models

OSS_PATH = 'https://images.guansong.wang'
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
    dir_path = models.CharField(max_length=128)
    first_path = models.CharField(max_length=16)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-dir_path',]
        verbose_name_plural = 'directories'

    def __str__(self):
        return self.dir_path

class Tag(models.Model):
    TAG_TYPE_CHOICES = (
        (1, 'Normal'),
        (2, 'Collection'),
        (3, 'Name'),
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
    file_name = models.CharField(max_length=128)
    taken_at = models.DateTimeField(null=True, blank=True)
    location = models.ForeignKey(Location, on_delete=models.CASCADE, default=0)
    title_en = models.CharField(max_length=128, blank=True)
    title_zh = models.CharField(max_length=128, blank=True)
    desc_en = models.TextField(blank=True)
    desc_zh = models.TextField(blank=True)
    favorite = models.BooleanField(default=False)
    hidden = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    tags = models.ManyToManyField(Tag)

    def __str__(self):
        return self.file_name
    def get_thumb(self):
        return OSS_PATH + self.file_name + '!' + THUMB_SUFFIX
    def get_preview(self):
        return OSS_PATH + self.file_name + '!' + PREVIEW_SUFFIX
    def get_original(self):
        return OSS_PATH + self.file_name + '!' + LARGE_SUFFIX
    def get_url(self):
        return OSS_PATH + self.file_name + '!' + LARGE_SUFFIX