# Generated by Django 4.1.7 on 2023-04-11 22:02

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('hello', '0003_post_log_date_post_owner_post_thumbnail'),
    ]

    operations = [
        migrations.CreateModel(
            name='AllCats',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('cat', models.CharField(max_length=80)),
                ('description', models.TextField()),
            ],
        ),
        migrations.CreateModel(
            name='PicSeries',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=80)),
                ('dateCreated', models.DateTimeField()),
                ('dateCaptured', models.DateTimeField()),
                ('dateModified', models.DateTimeField()),
                ('owner', models.CharField(max_length=80)),
                ('description', models.TextField()),
                ('heroIdBigPic', models.BigIntegerField(verbose_name='ID from Hero-BigPic')),
                ('heroIdThumbnail', models.BigIntegerField(verbose_name='ID from Hero-Thumbnail')),
                ('catPrime', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='hello.allcats')),
            ],
        ),
        migrations.CreateModel(
            name='SinglePic',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('bigPic', models.ImageField(upload_to='images/')),
                ('thumbnail', models.ImageField(upload_to='images/thumbnails')),
                ('series', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='hello.picseries')),
            ],
        ),
        migrations.CreateModel(
            name='SeriesCats',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('cat', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='hello.allcats')),
                ('series', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='hello.picseries')),
            ],
        ),
    ]
