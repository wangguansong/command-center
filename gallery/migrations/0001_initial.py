# Generated by Django 4.1 on 2022-09-07 07:06

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Directory',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('dir_path', models.CharField(max_length=128)),
                ('first_path', models.CharField(max_length=16)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
            ],
            options={
                'verbose_name_plural': 'directories',
                'ordering': ['-dir_path'],
            },
        ),
        migrations.CreateModel(
            name='Location',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('location', models.CharField(max_length=128, unique=True)),
                ('country_code', models.CharField(max_length=2)),
                ('title_en', models.CharField(max_length=128)),
                ('title_zh', models.CharField(max_length=128)),
                ('desc_en', models.TextField(blank=True)),
                ('desc_zh', models.TextField(blank=True)),
                ('latitude', models.DecimalField(blank=True, decimal_places=8, max_digits=10, null=True)),
                ('longitude', models.DecimalField(blank=True, decimal_places=8, max_digits=11, null=True)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
            ],
        ),
        migrations.CreateModel(
            name='Tag',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('tag', models.CharField(max_length=128, unique=True)),
                ('tag_type', models.SmallIntegerField(choices=[(1, 'Normal'), (2, 'Collection'), (3, 'Name')], default=0)),
                ('title_en', models.CharField(max_length=128)),
                ('title_zh', models.CharField(max_length=128)),
                ('desc_en', models.TextField(blank=True)),
                ('desc_zh', models.TextField(blank=True)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
            ],
        ),
        migrations.CreateModel(
            name='TagRelation',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('collection_tag', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='collection_tag', to='gallery.tag')),
                ('component_tag', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='component_tag', to='gallery.tag')),
            ],
            options={
                'db_table': 'gallery_tag_relation',
            },
        ),
        migrations.AddField(
            model_name='tag',
            name='components',
            field=models.ManyToManyField(through='gallery.TagRelation', to='gallery.tag'),
        ),
        migrations.CreateModel(
            name='Photo',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('file_name', models.CharField(max_length=128)),
                ('taken_at', models.DateTimeField(blank=True, null=True)),
                ('title_en', models.CharField(blank=True, max_length=128)),
                ('title_zh', models.CharField(blank=True, max_length=128)),
                ('desc_en', models.TextField(blank=True)),
                ('desc_zh', models.TextField(blank=True)),
                ('favorite', models.BooleanField(default=False)),
                ('hidden', models.BooleanField(default=True)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('directory', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='gallery.directory')),
                ('location', models.ForeignKey(default=0, on_delete=django.db.models.deletion.CASCADE, to='gallery.location')),
                ('tags', models.ManyToManyField(to='gallery.tag')),
            ],
        ),
    ]