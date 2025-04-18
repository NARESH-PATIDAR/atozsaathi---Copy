# Generated by Django 5.1.4 on 2025-03-06 06:34

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Chapter',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
            ],
        ),
        migrations.CreateModel(
            name='ClassName',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255, unique=True)),
                ('image', models.ImageField(upload_to='cards/images/')),
                ('card_color', models.CharField(default='#ffffff', max_length=7)),
            ],
        ),
        migrations.CreateModel(
            name='ContentCategory',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
            ],
        ),
        migrations.CreateModel(
            name='Heading',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=255)),
                ('underline', models.BooleanField(default=True)),
            ],
        ),
        migrations.CreateModel(
            name='Subject',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255, null=True, unique=True)),
            ],
        ),
        migrations.CreateModel(
            name='TitleClass',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('class_name', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='class_titles', to='educational.classname')),
                ('title', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='title_classes', to='educational.heading')),
            ],
            options={
                'unique_together': {('title', 'class_name')},
            },
        ),
        migrations.CreateModel(
            name='TitleClassSubChapter',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('chapter', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='title_class_subject_chapters', to='educational.chapter')),
            ],
        ),
        migrations.CreateModel(
            name='TitleClassSubChapterCategory',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('content_category', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='title_class_sub_chapter_categories', to='educational.contentcategory')),
                ('title_class_sub_chapter', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='categories', to='educational.titleclasssubchapter')),
            ],
            options={
                'unique_together': {('title_class_sub_chapter', 'content_category')},
            },
        ),
        migrations.CreateModel(
            name='ShortAnswer',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('question', models.TextField()),
                ('answer', models.TextField()),
                ('title_class_sub_chapter_category', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='short_answers', to='educational.titleclasssubchaptercategory')),
            ],
        ),
        migrations.CreateModel(
            name='MCQ',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('question', models.TextField()),
                ('option1', models.CharField(max_length=255)),
                ('option2', models.CharField(max_length=255)),
                ('option3', models.CharField(max_length=255)),
                ('option4', models.CharField(max_length=255)),
                ('correct_option', models.CharField(max_length=255)),
                ('title_class_sub_chapter_category', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='mcqs', to='educational.titleclasssubchaptercategory')),
            ],
        ),
        migrations.CreateModel(
            name='DetailedAnswer',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('question', models.TextField()),
                ('detailed_answer', models.TextField()),
                ('title_class_sub_chapter_category', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='detailed_answers', to='educational.titleclasssubchaptercategory')),
            ],
        ),
        migrations.CreateModel(
            name='CategoryQuestion',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('detailed_answer', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='educational.detailedanswer')),
                ('mcq', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='educational.mcq')),
                ('short_answer', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='educational.shortanswer')),
                ('title_class_sub_chapter_category', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='questions', to='educational.titleclasssubchaptercategory')),
            ],
        ),
        migrations.CreateModel(
            name='TitleClassSubject',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('subject', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='title_class_subjects', to='educational.subject')),
                ('title_class', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='subjects', to='educational.titleclass')),
            ],
            options={
                'unique_together': {('title_class', 'subject')},
            },
        ),
        migrations.AddField(
            model_name='titleclasssubchapter',
            name='title_class_subject',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='chapters', to='educational.titleclasssubject'),
        ),
        migrations.AlterUniqueTogether(
            name='titleclasssubchapter',
            unique_together={('title_class_subject', 'chapter')},
        ),
    ]
