# Generated by Django 4.0.4 on 2022-05-13 16:39

from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('myboardapp', '0004_alter_bulletin_file'),
    ]

    operations = [
        migrations.AddField(
            model_name='categorymodel',
            name='subscribers',
            field=models.ManyToManyField(blank=True, null=True, related_name='subscriber', to=settings.AUTH_USER_MODEL),
        ),
    ]
