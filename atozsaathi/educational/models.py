from django.db import models
from django.urls import reverse

class Heading(models.Model):
    title = models.CharField(max_length=255)
    underline = models.BooleanField(default=True)

    def __str__(self):
        return self.title

class ClassName(models.Model):
    name = models.CharField(max_length=255, unique=True)  # Unique class name
    image = models.ImageField(upload_to='cards/images/')
    card_color = models.CharField(max_length=7, default='#ffffff')  # Hex color code

     

    def __str__(self):
        return self.name

class Subject(models.Model):
    name = models.CharField(max_length=255, unique=True, null=True)  # Unique subject name

   

    def __str__(self):
        return self.name

class Chapter(models.Model):
    name = models.CharField(max_length=100)

     
    def __str__(self):
        return self.name

class ContentCategory(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name

class MCQ(models.Model):
    question = models.TextField()
    option1 = models.CharField(max_length=255)
    option2 = models.CharField(max_length=255)
    option3 = models.CharField(max_length=255)
    option4 = models.CharField(max_length=255)
    correct_option = models.CharField(max_length=255)
    title_class_sub_chapter_category = models.ForeignKey('TitleClassSubChapterCategory', on_delete=models.CASCADE, related_name='mcqs')

    def __str__(self):
        return self.question

class ShortAnswer(models.Model):
    question = models.TextField()
    answer = models.TextField()
    title_class_sub_chapter_category = models.ForeignKey('TitleClassSubChapterCategory', on_delete=models.CASCADE, related_name='short_answers')

    def __str__(self):
        return self.question

class DetailedAnswer(models.Model):
    question = models.TextField()
    detailed_answer = models.TextField()
    title_class_sub_chapter_category = models.ForeignKey('TitleClassSubChapterCategory', on_delete=models.CASCADE, related_name='detailed_answers')

    def __str__(self):
        return self.question

class TrueOrFalse(models.Model):
    question = models.TextField()
    is_true = models.BooleanField()
    title_class_sub_chapter_category = models.ForeignKey('TitleClassSubChapterCategory', on_delete=models.CASCADE, related_name='true_or_false')

    def __str__(self):
        return self.question

class FillInTheBlanks(models.Model):
    question = models.TextField()
    answer = models.TextField()
    title_class_sub_chapter_category = models.ForeignKey('TitleClassSubChapterCategory', on_delete=models.CASCADE, related_name='fill_in_the_blanks')

    def __str__(self):
        return self.question

class Notes(models.Model):
    title = models.CharField(max_length=255)
    content = models.TextField()
    title_class_sub_chapter_category = models.ForeignKey('TitleClassSubChapterCategory', on_delete=models.CASCADE, related_name='notes')

    def __str__(self):
        return self.title

class ChapterContent(models.Model):
    title = models.CharField(max_length=255)
    file = models.FileField(upload_to='chapter_contents/')
    title_class_sub_chapter_category = models.ForeignKey('TitleClassSubChapterCategory', on_delete=models.CASCADE, related_name='chapter_contents')

    def __str__(self):
        return self.title

class TitleClass(models.Model):
    title = models.ForeignKey(Heading, on_delete=models.CASCADE, related_name='title_classes')
    class_name = models.ForeignKey(ClassName, on_delete=models.CASCADE, related_name='class_titles')

    class Meta:
        unique_together = ('title', 'class_name')  # Prevent duplicate combinations

    def __str__(self):
        return f"{self.title.title} - {self.class_name.name}"

class TitleClassSubject(models.Model):
    title_class = models.ForeignKey(TitleClass, on_delete=models.CASCADE, related_name='subjects')
    subject = models.ForeignKey(Subject, on_delete=models.CASCADE, related_name='title_class_subjects')

    class Meta:
        unique_together = ('title_class', 'subject')  # Prevent duplicate combinations

    def __str__(self):
        return f"{self.title_class} - {self.subject.name}"

class TitleClassSubChapter(models.Model):
    title_class_subject = models.ForeignKey(TitleClassSubject, on_delete=models.CASCADE, related_name='chapters')
    chapter = models.ForeignKey(Chapter, on_delete=models.CASCADE, related_name='title_class_subject_chapters')

    class Meta:
        unique_together = ('title_class_subject', 'chapter')  # Prevent duplicate combinations

    def __str__(self):
        return f"{self.title_class_subject} - {self.chapter.name}"

class TitleClassSubChapterCategory(models.Model):
    title_class_sub_chapter = models.ForeignKey(TitleClassSubChapter, on_delete=models.CASCADE, related_name='categories')
    content_category = models.ForeignKey(ContentCategory, on_delete=models.CASCADE, related_name='title_class_sub_chapter_categories')

    class Meta:
        unique_together = ('title_class_sub_chapter', 'content_category')  # Prevent duplicate combinations

    def __str__(self):
        return f"{self.title_class_sub_chapter} - {self.content_category.name}"

class CategoryQuestion(models.Model):
    title_class_sub_chapter_category = models.ForeignKey(TitleClassSubChapterCategory, on_delete=models.CASCADE, related_name='questions')
    mcq = models.ForeignKey(MCQ, null=True, blank=True, on_delete=models.CASCADE)
    short_answer = models.ForeignKey(ShortAnswer, null=True, blank=True, on_delete=models.CASCADE)
    detailed_answer = models.ForeignKey(DetailedAnswer, null=True, blank=True, on_delete=models.CASCADE)
    true_or_false = models.ForeignKey(TrueOrFalse, null=True, blank=True, on_delete=models.CASCADE)
    fill_in_the_blanks = models.ForeignKey(FillInTheBlanks, null=True, blank=True, on_delete=models.CASCADE)
    notes = models.ForeignKey(Notes, null=True, blank=True, on_delete=models.CASCADE)
    chapter_content = models.ForeignKey(ChapterContent, null=True, blank=True, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.title_class_sub_chapter_category} - Question"

class ContactMessage(models.Model):
    name = models.CharField(max_length=100)
    email = models.EmailField()
    phone = models.CharField(max_length=20, blank=True)
    message = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Message from {self.name} ({self.email})"