# Generated by Django 2.0.1 on 2018-02-28 07:35

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('subject', '0016_auto_20180228_0734'),
    ]

    operations = [
        migrations.AlterField(
            model_name='groupsubject',
            name='parent',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='groups', to='subject.GroupSubject'),
        ),
    ]