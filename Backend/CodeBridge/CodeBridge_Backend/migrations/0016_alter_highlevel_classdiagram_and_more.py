# Generated by Django 4.1.11 on 2023-11-03 06:22

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('CodeBridge_Backend', '0015_highlevel'),
    ]

    operations = [
        migrations.AlterField(
            model_name='highlevel',
            name='classDiagram',
            field=models.TextField(null=True),
        ),
        migrations.AlterField(
            model_name='highlevel',
            name='flowChart',
            field=models.TextField(null=True),
        ),
    ]