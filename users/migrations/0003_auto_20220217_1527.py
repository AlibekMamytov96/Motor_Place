# Generated by Django 3.1 on 2022-02-17 09:27

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0002_auto_20220217_1526'),
    ]

    operations = [
        migrations.RenameField(
            model_name='myuser',
            old_name='isBuyer',
            new_name='isSeller',
        ),
    ]
