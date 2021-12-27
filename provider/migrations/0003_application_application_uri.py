# Generated by Django 3.1.7 on 2021-04-01 09:00

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('provider', '0002_auto_20210323_0942'),
    ]

    operations = [
        migrations.AddField(
            model_name='application',
            name='application_uri',
            field=models.TextField(blank=True, help_text='URL of the application; include port number if application is IP hosted'),
        ),
    ]
