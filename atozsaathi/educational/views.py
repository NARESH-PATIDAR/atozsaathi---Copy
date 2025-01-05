from django.shortcuts import render
from django.http import HttpResponse
from .models import Heading

# Create your views here.
def index(request):
    return render(request, 'educational/index.html')


def home(request):
    headings = Heading.objects.prefetch_related('cards').all()
    return render(request, 'educational/home.html', {'headings': headings})



def contact(request):
    return render(request, 'educational/contact.html')

def about(request):
    return render(request, 'educational/about.html')

def subject(request):
    return render(request, 'educational/subject.html')

def stream(request):
    return render(request, 'educational/stream.html')
