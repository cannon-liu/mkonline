# Generated by Django 2.0.6 on 2018-06-22 09:34

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('user', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='userprofile',
            name='image',
            field=models.ImageField(default='static/image/default.png', upload_to='image/%Y/%m', verbose_name='头像'),
        ),
    ]