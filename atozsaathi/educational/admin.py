from django.contrib import admin
from .models import  *
class ChapterInline(admin.TabularInline):
    model = TitleClassSubChapter
    extra = 1  # Number of extra forms to display

class TitleClassSubjectAdmin(admin.ModelAdmin):
    inlines = [ChapterInline]

class TitleClassInline(admin.TabularInline):
    model = TitleClass
    extra = 1

class HeadingAdmin(admin.ModelAdmin):
    inlines = [TitleClassInline]

class TitleClassSubjectInline(admin.TabularInline):
    model = TitleClassSubject
    extra = 1

class TitleClassAdmin(admin.ModelAdmin):
    inlines = [TitleClassSubjectInline]

class TitleClassSubChapterCategoryInline(admin.TabularInline):
    model = TitleClassSubChapterCategory
    extra = 1

class TitleClassSubChapterAdmin(admin.ModelAdmin):
    inlines = [TitleClassSubChapterCategoryInline]

class CategoryQuestionInline(admin.TabularInline):
    model = CategoryQuestion
    extra = 1

class TitleClassSubChapterCategoryAdmin(admin.ModelAdmin):
    inlines = [CategoryQuestionInline]


admin.site.register(ContactMessage)
admin.site.register(Heading, HeadingAdmin)
admin.site.register(ClassName)
admin.site.register(Subject)
admin.site.register(Chapter)
admin.site.register(ContentCategory)
admin.site.register(MCQ)
admin.site.register(ShortAnswer)
admin.site.register(DetailedAnswer)

admin.site.register(TrueOrFalse)
admin.site.register(FillInTheBlanks)
admin.site.register(Notes)
admin.site.register(ChapterContent)


admin.site.register(TitleClass, TitleClassAdmin)
admin.site.register(TitleClassSubject, TitleClassSubjectAdmin)
admin.site.register(TitleClassSubChapter, TitleClassSubChapterAdmin)
admin.site.register(TitleClassSubChapterCategory, TitleClassSubChapterCategoryAdmin)


