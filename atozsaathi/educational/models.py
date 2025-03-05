from django.db import models

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

class ClassHeading(models.Model):
    class_name = models.ForeignKey(ClassName, related_name="class_headings", on_delete=models.CASCADE)
    heading = models.ForeignKey(Heading, related_name="class_headings", on_delete=models.CASCADE)

    class Meta:
        unique_together = ('class_name', 'heading')  # Prevent duplicate combinations

    def __str__(self):
        return f"{self.class_name.name} - {self.heading.title}"

class ClassSubject(models.Model):
    class_name = models.ForeignKey(ClassName, related_name="class_subjects", on_delete=models.CASCADE, null=True, blank=True)
    subject = models.ForeignKey(Subject, related_name="class_subjects", on_delete=models.CASCADE)
    heading = models.ForeignKey(Heading, related_name="class_subjects", on_delete=models.CASCADE, null=True, blank=True)

    class Meta:
        unique_together = ('class_name', 'subject', 'heading')  # Prevent duplicate combinations

    def __str__(self):
        return f"{self.class_name.name} - {self.subject.name} ({self.heading.title})"

class Material(models.Model):
    class_subject = models.ForeignKey(ClassSubject, related_name="materials", on_delete=models.CASCADE)
    title = models.CharField(max_length=255)
    content = models.TextField()

    def __str__(self):
        return self.title

 

class Chapter(models.Model):
    name = models.CharField(max_length=100)
    subject = models.ForeignKey(Subject, related_name='chapters', on_delete=models.CASCADE)
    content_categories = models.ManyToManyField('ContentCategory', related_name='chapters')

    def __str__(self):
        return self.name

class ContentCategory(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name
class ClassSubjectChapter(models.Model):
    class_name = models.ForeignKey(ClassName, related_name="class_subject_chapters", on_delete=models.CASCADE)
    subject = models.ForeignKey(Subject, related_name="class_subject_chapters", on_delete=models.CASCADE)
    chapter = models.ForeignKey(Chapter, related_name="class_subject_chapters", on_delete=models.CASCADE)

    class Meta:
        unique_together = ('class_name', 'subject', 'chapter')  # Prevent duplicate combinations

    def __str__(self):
        return f"{self.class_name.name} - {self.subject.name} - {self.chapter.name}"