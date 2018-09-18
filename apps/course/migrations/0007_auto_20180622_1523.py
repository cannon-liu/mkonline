# Generated by Django 2.0.6 on 2018-06-22 15:23

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('course', '0006_auto_20180622_1439'),
    ]

    operations = [
        migrations.AddField(
            model_name='video',
            name='has_learned',
            field=models.BooleanField(default=False, verbose_name='是否学习'),
        ),
        migrations.AddField(
            model_name='video',
            name='play_time',
            field=models.IntegerField(default=0, verbose_name='学习时长(分钟数)'),
        ),
        migrations.AddField(
            model_name='video',
            name='url',
            field=models.CharField(default='', max_length=200, verbose_name='访问地址'),
        ),
    ]
