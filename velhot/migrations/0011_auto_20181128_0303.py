# Generated by Django 2.1.2 on 2018-11-28 01:03

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('velhot', '0010_auto_20181127_1536'),
    ]

    operations = [
        migrations.AlterField(
            model_name='chat',
            name='message',
            field=models.CharField(max_length=255, null=True),
        ),
    ]