# Generated by Django 5.0.6 on 2024-06-08 11:28

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('login', '0008_alter_note_file'),
    ]

    operations = [
        migrations.CreateModel(
            name='Feedback',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
                ('email', models.EmailField(max_length=254)),
                ('feedback', models.TextField()),
                ('created_at', models.DateTimeField(auto_now_add=True)),
            ],
        ),
    ]
