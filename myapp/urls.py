from django.urls import path
from myapp import views

app_name = 'myapp'

urlpatterns = [
    path('', views.index, name='index'),  # Landing Page
    path('about/', views.about, name='about'),  # About Page (Restored)
    path('<int:cat_no>/', views.detail, name='detail'),  # Category Detail Page
]