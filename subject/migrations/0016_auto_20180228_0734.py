# Generated by Django 2.0.1 on 2018-02-28 07:34

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('subject', '0015_auto_20180224_0247'),
    ]

    operations = [
        migrations.AlterField(
            model_name='groupsubject',
            name='parent',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='group', to='subject.GroupSubject'),
        ),
    ]