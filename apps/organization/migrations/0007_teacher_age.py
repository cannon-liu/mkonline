# Generated by Django 2.0.6 on 2018-06-26 16:00

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('organization', '0006_auto_20180620_2140'),
    ]

    operations = [
        migrations.AddField(
            model_name='teacher',
            name='age',
            field=models.IntegerField(blank=True, null=True, verbose_name='收藏人数'),
        ),
    ]