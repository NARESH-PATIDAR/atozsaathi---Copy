from django.urls import path
from . import views
 

urlpatterns = [
      path('', views.index, name='index'),
      path('home/', views.home, name='home'),
      path('contact/', views.contact, name='contact'),
      path('about/', views.about, name='about'),
      path('subject/', views.subject, name='subject'),
      path('stream/', views.stream, name='stream'),
      
    
]