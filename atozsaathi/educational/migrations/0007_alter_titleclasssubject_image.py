# Generated by Django 5.1.4 on 2025-04-08 18:17

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('educational', '0006_alter_titleclasssubject_image'),
    ]

    operations = [
        migrations.AlterField(
            model_name='titleclasssubject',
            name='image',
            field=models.ImageField(blank=True, default='title_class_subject_images/default.png', upload_to='title_class_subject_images/'),
        ),
    ]
