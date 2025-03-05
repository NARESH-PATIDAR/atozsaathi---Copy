from django.shortcuts import get_object_or_404, render
from django.http import HttpResponse
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
    class_subject_chapters = ClassSubjectChapter.objects.filter(class_name_id=class_id, subject_id=subject_id)
    return render(request, 'educational/subject_detail.html', {'subject': subject, 'class_subject_chapters': class_subject_chapters})