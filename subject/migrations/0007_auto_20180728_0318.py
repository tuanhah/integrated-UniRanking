# Generated by Django 2.0.4 on 2018-07-28 03:18

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('subject', '0006_auto_20180709_1703'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='sector',
            options={'ordering': ['id'], 'verbose_name': 'Nhóm ngành', 'verbose_name_plural': 'Các nhóm ngành'},
        ),
        migrations.AlterModelOptions(
            name='universitysector',
            options={'ordering': ['id'], 'verbose_name': 'Đại học - Nhóm ngành', 'verbose_name_plural': 'Đại học - Nhóm ngành'},
        ),
    ]