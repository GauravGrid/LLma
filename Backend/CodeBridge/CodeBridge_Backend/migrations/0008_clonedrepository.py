# Generated by Django 4.1.10 on 2023-09-07 10:53

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('CodeBridge_Backend', '0007_user_access_token'),
    ]

    operations = [
        migrations.CreateModel(
            name='ClonedRepository',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('repository_name', models.CharField(max_length=256)),
                ('repository_url', models.URLField()),
                ('branch', models.CharField(max_length=100)),
                ('last_updated', models.DateTimeField(auto_now=True)),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='CodeBridge_Backend.user')),
            ],
        ),
    ]