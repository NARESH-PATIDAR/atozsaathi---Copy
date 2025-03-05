# Generated by Django 5.1.4 on 2025-03-05 07:49

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('educational', '0004_remove_chapter_subject_classsubjectchapter'),
    ]

    operations = [
        migrations.CreateModel(
            name='ContentCategory',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
            ],
        ),
        migrations.AlterField(
            model_name='chapter',
            name='name',
            field=models.CharField(max_length=100),
        ),
        migrations.AddField(
            model_name='chapter',
            name='content_categories',
            field=models.ManyToManyField(related_name='chapters', to='educational.contentcategory'),
        ),
    ]
