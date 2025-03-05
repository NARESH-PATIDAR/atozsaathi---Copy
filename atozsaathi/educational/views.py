from django.shortcuts import get_object_or_404, render
from django.http import HttpResponse, JsonResponse
from .models import *

# Create your views here.
def index(request):
    return render(request, 'educational/index.html')

def home(request):
    headings = Heading.objects.prefetch_related('class_headings__class_name').all()
    return render(request, 'educational/home.html', {'headings': headings})

def contact(request):
    return render(request, 'educational/contact.html')

def about(request):
    return render(request, 'educational/about.html')

def stream(request):
    return render(request, 'educational/stream.html')


def subjects(request, class_id, heading_id):
    class_obj = get_object_or_404(ClassName, id=class_id)
    heading = get_object_or_404(Heading, id=heading_id)
    subjects = ClassSubject.objects.filter(class_name=class_obj, heading=heading)
    return render(request, 'educational/subjects.html', {'class_obj': class_obj, 'heading': heading, 'subjects': subjects})

def subclass(request, class_id):
    class_obj = get_object_or_404(ClassName, id=class_id)
    # Add logic to fetch sub-classes if needed
    return render(request, 'educational/subclass.html', {'class_obj': class_obj})


def subject_detail(request, class_id, subject_id):
    subject = get_object_or_404(Subject, id=subject_id)
    class_obj = get_object_or_404(ClassName, id=class_id)
    class_subject_chapters = ClassSubjectChapter.objects.filter(class_name=class_obj, subject=subject)
    context = {
        'subject': subject,
        'class_subject_chapters': class_subject_chapters,
    }
    return render(request, 'educational/subject_detail.html', context)


def get_chapter_categories(request, chapter_id):
    try:
        chapter = Chapter.objects.get(id=chapter_id)
        categories = chapter.content_categories.all()
        categories_data = [{'name': category.name} for category in categories]
        return JsonResponse({'categories': categories_data})
    except Chapter.DoesNotExist:
        return JsonResponse({'error': 'Chapter not found'}, status=404)
 

def get_category_content(request, chapter_id, category_name):
    chapter = get_object_or_404(Chapter, id=chapter_id)
    content_category = get_object_or_404(ContentCategory, name=category_name)
    
    content_links = ContentLink.objects.filter(chapter=chapter, content_category=content_category)
    content_data = []

    for link in content_links:
        if link.content_type == 'mcq':
            content = MCQ.objects.get(id=link.content_id)
            content_data.append({
                'type': 'mcq',
                'question': content.question,
                'option1': content.option1,
                'option2': content.option2,
                'option3': content.option3,
                'option4': content.option4,
                'correct_option': content.correct_option
            })
        elif link.content_type == 'short_answer':
            content = ShortAnswer.objects.get(id=link.content_id)
            content_data.append({
                'type': 'short_answer',
                'question': content.question,
                'answer': content.answer
            })
        elif link.content_type == 'detailed_answer':
            content = DetailedAnswer.objects.get(id=link.content_id)
            content_data.append({
                'type': 'detailed_answer',
                'question': content.question,
                'detailed_answer': content.answer
            })
        else:
            continue

    return JsonResponse({'content': content_data})
    
