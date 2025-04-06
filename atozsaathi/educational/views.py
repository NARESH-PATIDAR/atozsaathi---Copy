from django.shortcuts import get_object_or_404, render
from django.http import JsonResponse
from .models import Heading, ClassName, Subject, Chapter, ContentCategory, TitleClass, TitleClassSubject, TitleClassSubChapter, TitleClassSubChapterCategory, CategoryQuestion, MCQ, ShortAnswer, DetailedAnswer, TrueOrFalse, FillInTheBlanks, Notes, ChapterContent

# Create your views here.
def index(request):
    return render(request, 'educational/index.html')

def home(request):
    headings = Heading.objects.prefetch_related('title_classes__class_name').all()
    context = {'headings': headings}
    return render(request, 'educational/home.html', context)

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