# Generated by Django 3.1.3 on 2021-03-03 12:03

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('chat', '0003_auto_20210303_1327'),
    ]

    operations = [
        migrations.AddField(
            model_name='message',
            name='reciever',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='Reciever', to=settings.AUTH_USER_MODEL),
        ),
    ]
