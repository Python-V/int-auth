# Generated by Django 3.1.7 on 2021-03-30 07:37

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('auth', '0012_alter_user_first_name_max_length'),
        ('provider', '0002_auto_20210323_0942'),
        ('users', '0001_initial'),
    ]

    operations = [
        migrations.AlterUniqueTogether(
            name='viewgrouppermission',
            unique_together={('group', 'view_name', 'application', 'permission')},
        ),
    ]
