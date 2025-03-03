from django.urls import path
from myapp import views

app_name = 'myapp'

urlpatterns = [
    path('', views.index, name='index'),  # Landing Page
    path('about/', views.about, name='about'),  # About Page (Restored)
    path('<int:cat_no>/', views.detail, name='detail'),  # Category Detail Page
    path('products/', views.products, name='products'),  # URL for products page
    path('place_order/', views.place_order, name='place_order'),  # URL for order placement
    path('products/<int:prod_id>/', views.productdetail, name='productdetail'),  # Product Detail Page
    
]