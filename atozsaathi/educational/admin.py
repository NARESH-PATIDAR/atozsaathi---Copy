from django.contrib import admin
from .models import *

# Register your models here.
admin.site.register(Heading)
admin.site.register(ClassName)
admin.site.register(Subject)
admin.site.register(ClassSubject)
admin.site.register(ClassHeading)
admin.site.register(Material)
admin.site.register(Chapter)
admin.site.register(ClassSubjectChapter)
admin.site.register(ContentCategory)

