from django.shortcuts import get_object_or_404, render
from django.http import JsonResponse
from django.db.models import Q

from .models import Heading, ClassName, Subject, Chapter, ContentCategory, TitleClass, TitleClassSubject, TitleClassSubChapter, TitleClassSubChapterCategory, CategoryQuestion, MCQ, ShortAnswer, DetailedAnswer, TrueOrFalse, FillInTheBlanks, Notes, ChapterContent

# Create your views here.
def index(request):
    return render(request, 'educational/index.html')

def home(request):
    headings = Heading.objects.prefetch_related('title_classes__class_name').all()
    context = {'headings': headings}
    return render(request, 'educational/home.html', context)

def search_all(request):
    query = request.GET.get('q', '').strip().lower()
    results = []

    if not query:
        return JsonResponse({'results': results})

    # 1. Search in Heading
    headings = Heading.objects.filter(title__icontains=query)
    for heading in headings:
        for title_class in heading.title_classes.all():
            results.append({
                'display': f"{heading.title} > {title_class.class_name.name}",
                'url': f"/class/{title_class.class_name.id}/heading/{heading.id}/subjects/"
            })

    if results:
        return JsonResponse({'results': results})

    # 2. Search in ClassName
    classes = ClassName.objects.filter(name__icontains=query)
    for class_obj in classes:
        title_classes = TitleClass.objects.filter(class_name=class_obj).select_related('title')
        for title_class in title_classes:
            results.append({
                'display': f"{title_class.title.title} > {class_obj.name}",
                'url': f"/class/{class_obj.id}/heading/{title_class.title.id}/subjects/"
            })

    if results:
        return JsonResponse({'results': results})

    # 3. Search in Subject
    subjects = Subject.objects.filter(name__icontains=query)
    for subject in subjects:
        title_class_subjects = TitleClassSubject.objects.filter(subject=subject).select_related(
            'title_class__title', 'title_class__class_name'
        )
        for tcs in title_class_subjects:
            heading = tcs.title_class.title
            class_name = tcs.title_class.class_name
            results.append({
                'display': f"{heading.title} > {class_name.name} > {subject.name}",
                'url': f"/class/{class_name.id}/subject/{subject.id}/"
            })

    if results:
        return JsonResponse({'results': results})

    # 4. Search in Chapter
    chapters = Chapter.objects.filter(name__icontains=query)
    for chapter in chapters:
        subchapters = TitleClassSubChapter.objects.filter(chapter=chapter).select_related(
            'title_class_subject__subject',
            'title_class_subject__title_class__title',
            'title_class_subject__title_class__class_name'
        )
        for sc in subchapters:
            heading = sc.title_class_subject.title_class.title
            class_name = sc.title_class_subject.title_class.class_name
            subject = sc.title_class_subject.subject
            results.append({
                'display': f"{heading.title} > {class_name.name} > {subject.name} > {chapter.name}",
                'url': f"/class/{class_name.id}/subject/{subject.id}/"
            })

    return JsonResponse({'results': results})


def contact(request):
    return render(request, 'educational/contact.html')

def about(request):
    return render(request, 'educational/about.html')

def stream(request):
    return render(request, 'educational/stream.html')

def subjects(request, class_id, heading_id):
    class_obj = get_object_or_404(ClassName, id=class_id)
    heading = get_object_or_404(Heading, id=heading_id)
    title_class = get_object_or_404(TitleClass, title=heading, class_name=class_obj)
    subjects = TitleClassSubject.objects.filter(title_class=title_class)
    return render(request, 'educational/subjects.html', {'class_obj': class_obj, 'heading': heading, 'subjects': subjects})

def subclass(request, class_id):
    class_obj = get_object_or_404(ClassName, id=class_id)
    # Add logic to fetch sub-classes if needed
    return render(request, 'educational/subclass.html', {'class_obj': class_obj})

def subject_detail(request, class_id, subject_id):
    subject = get_object_or_404(Subject, id=subject_id)
    class_obj = get_object_or_404(ClassName, id=class_id)
    title_class = get_object_or_404(TitleClass, class_name=class_obj)
    title_class_subject = get_object_or_404(TitleClassSubject, title_class=title_class, subject=subject)
    class_subject_chapters = TitleClassSubChapter.objects.filter(title_class_subject=title_class_subject)
    context = {
        'subject': subject,
        'class_subject_chapters': class_subject_chapters,
    }
    return render(request, 'educational/subject_detail.html', context)

def get_chapter_categories(request, chapter_id):
    try:
        chapter = Chapter.objects.get(id=chapter_id)
        title_class_sub_chapter_categories = TitleClassSubChapterCategory.objects.filter(title_class_sub_chapter__chapter=chapter)
        categories = [tcsc.content_category for tcsc in title_class_sub_chapter_categories]
        categories_data = [{'id': category.id, 'name': category.name} for category in categories]
        return JsonResponse({'categories': categories_data})
    except Chapter.DoesNotExist:
        return JsonResponse({'error': 'Chapter not found'}, status=404)

def get_category_content(request, chapter_id, category_id):
    print(f"Fetching content for chapter_id: {chapter_id}, category_id: {category_id}")
    
    title_class_sub_chapter_category = get_object_or_404(TitleClassSubChapterCategory,
        title_class_sub_chapter__chapter_id=chapter_id,
        content_category_id=category_id
    )
    
    print(f"Found TitleClassSubChapterCategory: {title_class_sub_chapter_category}")
    
    mcqs = MCQ.objects.filter(title_class_sub_chapter_category=title_class_sub_chapter_category)
    short_answers = ShortAnswer.objects.filter(title_class_sub_chapter_category=title_class_sub_chapter_category)
    detailed_answers = DetailedAnswer.objects.filter(title_class_sub_chapter_category=title_class_sub_chapter_category)
    true_or_false_questions = TrueOrFalse.objects.filter(title_class_sub_chapter_category=title_class_sub_chapter_category)
    fill_in_the_blanks_questions = FillInTheBlanks.objects.filter(title_class_sub_chapter_category=title_class_sub_chapter_category)
    notes = Notes.objects.filter(title_class_sub_chapter_category=title_class_sub_chapter_category)
    chapter_contents = ChapterContent.objects.filter(title_class_sub_chapter_category=title_class_sub_chapter_category)
    
    content_data = []

    for mcq in mcqs:
        content_data.append({
            'type': 'mcq',
            'question': mcq.question,
            'option1': mcq.option1,
            'option2': mcq.option2,
            'option3': mcq.option3,
            'option4': mcq.option4,
            'correct_option': mcq.correct_option
        })
    
    for short_answer in short_answers:
        content_data.append({
            'type': 'short_answer',
            'question': short_answer.question,
            'answer': short_answer.answer
        })
    
    for detailed_answer in detailed_answers:
        content_data.append({
            'type': 'detailed_answer',
            'question': detailed_answer.question,
            'detailed_answer': detailed_answer.detailed_answer
        })
    
    for true_or_false in true_or_false_questions:
        content_data.append({
            'type': 'true_or_false',
            'question': true_or_false.question,
            'is_true': true_or_false.is_true
        })
    
    for fill_in_the_blank in fill_in_the_blanks_questions:
        content_data.append({
            'type': 'fill_in_the_blanks',
            'question': fill_in_the_blank.question,
            'answer': fill_in_the_blank.answer
        })
    
    for note in notes:
        content_data.append({
            'type': 'notes',
            'title': note.title,
            'content': note.content
        })
    
    for chapter_content in chapter_contents:
        content_data.append({
            'type': 'chapter_content',
            'title': chapter_content.title,
            'file_url': chapter_content.file.url
        })

    print(f"Content data: {content_data}")

    return JsonResponse({'content': content_data})