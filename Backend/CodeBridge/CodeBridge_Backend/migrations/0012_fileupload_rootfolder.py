# Generated by Django 4.1.10 on 2023-09-20 06:53

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('CodeBridge_Backend', '0011_alter_githubrepository_source_code'),
    ]

    operations = [
        migrations.AddField(
            model_name='fileupload',
            name='rootFolder',
            field=models.IntegerField(null=True),
        ),
    ]