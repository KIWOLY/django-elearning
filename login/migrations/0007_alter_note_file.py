# Generated by Django 5.0.6 on 2024-06-07 18:31

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('login', '0006_note'),
    ]

    operations = [
        migrations.AlterField(
            model_name='note',
            name='file',
            field=models.FileField(upload_to='media/notes/'),
        ),
    ]