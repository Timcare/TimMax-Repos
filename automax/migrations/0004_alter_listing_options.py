# Generated by Django 4.2.2 on 2023-11-10 18:03

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('automax', '0003_alter_listing_options'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='listing',
            options={'ordering': ('updated_at',)},
        ),
    ]
