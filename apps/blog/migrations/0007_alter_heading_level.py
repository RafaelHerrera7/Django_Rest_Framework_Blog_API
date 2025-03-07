# Generated by Django 4.2.16 on 2025-03-07 18:16

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0006_alter_heading_level'),
    ]

    operations = [
        migrations.AlterField(
            model_name='heading',
            name='level',
            field=models.IntegerField(choices=[(1, 'H1'), (2, 'H2'), (3, 'H3'), (4, 'H4'), (5, 'H5'), (6, 'H6')]),
        ),
    ]
