# Generated by Django 4.1 on 2022-09-27 08:38

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('post', '0014_profile'),
    ]

    operations = [
        migrations.AlterField(
            model_name='stream',
            name='date',
            field=models.DateTimeField(auto_now=True),
        ),
        migrations.AlterField(
            model_name='stream',
            name='user',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='stream_user', to=settings.AUTH_USER_MODEL),
        ),
    ]
