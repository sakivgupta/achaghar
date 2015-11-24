# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        ('contenttypes', '0002_remove_content_type_name'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Address',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('add1', models.CharField(max_length=50)),
                ('add2', models.CharField(max_length=50, null=True, blank=True)),
                ('pincode', models.CharField(help_text=b'Pincode must be Six digits only', max_length=6, verbose_name=b'Pincode')),
                ('city', models.CharField(max_length=50, verbose_name=b'City', blank=True)),
                ('locality', models.CharField(max_length=50, verbose_name=b'Locality', blank=True)),
                ('state', models.CharField(max_length=50, verbose_name=b'State', blank=True)),
            ],
        ),
        migrations.CreateModel(
            name='Category',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('post_type', models.CharField(default=b'F', max_length=1, verbose_name=b'Post Type', choices=[(b'F', b'Flat'), (b'PG-G', b'PG Girls'), (b'PG-B', b'PG Boys'), (b'R', b'Rooms')])),
            ],
        ),
        migrations.CreateModel(
            name='Country',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('country', models.CharField(default=b'India', max_length=30, verbose_name=b'Country')),
                ('flag', models.CharField(max_length=10, null=True, verbose_name=b'Flag Icons', blank=True)),
                ('tel_code', models.CharField(max_length=10, null=True, verbose_name=b'Telephone Codes', blank=True)),
                ('currency', models.CharField(default=b'INR', max_length=20, null=True, verbose_name=b'Default Currency', blank=True)),
            ],
        ),
        migrations.CreateModel(
            name='Image',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('object_id', models.PositiveIntegerField()),
                ('image', models.ImageField(upload_to=b'/images/')),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='Post',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('features', models.CharField(max_length=200, verbose_name=b'Add Features')),
                ('current_residents', models.IntegerField(default=0, verbose_name=b'Current Residents', blank=True)),
                ('residents_info', models.CharField(max_length=100, verbose_name=b'Residents Information')),
                ('looking_for_info', models.CharField(max_length=200, verbose_name=b'Looking For')),
                ('rent', models.IntegerField()),
                ('flat_type', models.CharField(default=b'1 BHK', max_length=10, null=True, blank=True)),
                ('add_payment', models.CharField(max_length=100, null=True, verbose_name=b'Additional Payment', blank=True)),
                ('services', models.CharField(max_length=200, null=True, blank=True)),
                ('alternate_mobile', models.IntegerField(help_text=b'Phone number must be 10 digits entered without +91', null=True, verbose_name=b'Alternate Mobile', blank=True)),
                ('category', models.ForeignKey(to='postadd.Category')),
                ('creator', models.ForeignKey(related_name='postadd_post_created_by', to=settings.AUTH_USER_MODEL)),
                ('editor', models.ForeignKey(related_name='postadd_post_last_modified', blank=True, to=settings.AUTH_USER_MODEL, null=True)),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='Reviews',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('object_id', models.PositiveIntegerField()),
                ('review', models.CharField(max_length=100)),
                ('content_type', models.ForeignKey(to='contenttypes.ContentType')),
                ('room', models.ForeignKey(to='postadd.Post')),
                ('user', models.ForeignKey(to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Type',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('user_type', models.CharField(default=b'O', max_length=1, choices=[(b'B', b'Broker'), (b'O', b'Owner'), (b'FR', b'Flatmate Required')])),
            ],
        ),
        migrations.CreateModel(
            name='UserProfile',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('mobile', models.IntegerField(help_text=b'Phone number must be 10 digits entered without +91', verbose_name=b'Mobile Number')),
                ('phone', models.CharField(max_length=15, null=True, blank=True)),
                ('ip', models.CharField(default=b'', max_length=50, null=True, blank=True)),
                ('subscribed', models.BooleanField(default=True)),
                ('info', models.CharField(max_length=100, null=True, blank=True)),
                ('address', models.ForeignKey(blank=True, to='postadd.Address', null=True)),
                ('country', models.ForeignKey(default=b'India', to='postadd.Country')),
                ('creator', models.ForeignKey(related_name='postadd_userprofile_created_by', to=settings.AUTH_USER_MODEL)),
                ('editor', models.ForeignKey(related_name='postadd_userprofile_last_modified', blank=True, to=settings.AUTH_USER_MODEL, null=True)),
                ('user', models.ForeignKey(to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'ordering': ['user'],
            },
        ),
        migrations.CreateModel(
            name='ImageAltHref',
            fields=[
                ('image_ptr', models.OneToOneField(parent_link=True, auto_created=True, primary_key=True, serialize=False, to='postadd.Image')),
                ('alt', models.CharField(default=b'', max_length=50, blank=True, help_text=b'Text to display in case image does not load', null=True, verbose_name=b'Alt text')),
                ('href', models.CharField(default=b'', max_length=200, blank=True, help_text=b'Enter full URL to link to, with trailing slash (e.g. http://www.achaghar.com/xyz/)', null=True, verbose_name=b'URL')),
            ],
            options={
                'ordering': ('id',),
                'verbose_name': 'Image Link',
            },
            bases=('postadd.image',),
        ),
        migrations.AddField(
            model_name='post',
            name='images',
            field=models.ManyToManyField(default=None, help_text=b'', related_name='room_images', to='postadd.Image', blank=True),
        ),
        migrations.AddField(
            model_name='post',
            name='location',
            field=models.ForeignKey(to='postadd.Address'),
        ),
        migrations.AddField(
            model_name='post',
            name='user',
            field=models.ForeignKey(verbose_name=b'Add Posted By', to='postadd.UserProfile'),
        ),
        migrations.AddField(
            model_name='post',
            name='user_type',
            field=models.ForeignKey(to='postadd.Type'),
        ),
        migrations.AddField(
            model_name='image',
            name='content_type',
            field=models.ForeignKey(to='contenttypes.ContentType'),
        ),
        migrations.AddField(
            model_name='address',
            name='country',
            field=models.ForeignKey(to='postadd.Country'),
        ),
        migrations.AlterUniqueTogether(
            name='reviews',
            unique_together=set([('user', 'room')]),
        ),
        migrations.AlterUniqueTogether(
            name='image',
            unique_together=set([('content_type', 'object_id')]),
        ),
    ]
