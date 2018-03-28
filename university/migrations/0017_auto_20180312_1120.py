# Generated by Django 2.0.1 on 2018-03-12 11:20

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('criteria', '0004_auto_20180224_0247'),
        ('university', '0016_auto_20180312_0836'),
    ]

    operations = [
        migrations.AlterUniqueTogether(
            name='universityscore',
            unique_together={('score_by_category', 'criterion')},
        ),
        migrations.AlterUniqueTogether(
            name='universityscorebycategory',
            unique_together={('university', 'category_criterion')},
        ),
    ]
