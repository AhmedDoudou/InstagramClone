# Generated by Django 4.1 on 2022-09-25 21:53

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('post', '0012_remove_post_comments'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='post',
            name='text',
        ),
    ]
