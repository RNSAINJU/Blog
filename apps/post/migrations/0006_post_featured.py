# Generated by Django 2.2.1 on 2019-09-19 14:34

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('post', '0005_auto_20190919_2017'),
    ]

    operations = [
        migrations.AddField(
            model_name='post',
            name='featured',
            field=models.BooleanField(default=False),
            preserve_default=False,
        ),
    ]
