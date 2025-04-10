# Generated by Django 5.1.4 on 2025-04-06 17:09

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('educational', '0002_chaptercontent_categoryquestion_chapter_content_and_more'),
    ]

    operations = [
        migrations.CreateModel(
            name='ContactMessage',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
                ('email', models.EmailField(max_length=254)),
                ('phone', models.CharField(blank=True, max_length=20)),
                ('message', models.TextField()),
                ('created_at', models.DateTimeField(auto_now_add=True)),
            ],
        ),
    ]
