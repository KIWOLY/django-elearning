# Generated by Django 5.0.6 on 2024-06-07 18:37

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('login', '0007_alter_note_file'),
    ]

    operations = [
        migrations.AlterField(
            model_name='note',
            name='file',
            field=models.FileField(upload_to='notes/'),
        ),
    ]
