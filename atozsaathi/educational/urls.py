from django.urls import path
from . import views
 

urlpatterns = [
      path('', views.index, name='index'),
      path('home/', views.home, name='home'),
      path('contact/', views.contact, name='contact'),
      path('about/', views.about, name='about'),
      path('stream/', views.stream, name='stream'),
      
      
      path('subjects/<int:class_id>/', views.subjects, name='subjects'),
      path('subclass/<int:class_id>/', views.subclass, name='subclass'),
      path('subject/<int:subject_id>/', views.subject_detail, name='subject_detail'),

      path('class/<int:class_id>/heading/<int:heading_id>/subjects/', views.subjects, name='subjects'),
      path('class/<int:class_id>/subject/<int:subject_id>/', views.subject_detail, name='subject_detail'), 
    
]