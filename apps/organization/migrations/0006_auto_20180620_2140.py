# Generated by Django 2.0.6 on 2018-06-20 21:40

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('organization', '0005_auto_20180620_1655'),
    ]

    operations = [
        migrations.AlterField(
            model_name='teacher',
            name='image',
            field=models.ImageField(upload_to='teacher/%Y/%m', verbose_name='教师图片'),
        ),
    ]