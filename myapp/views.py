from django.http import HttpResponse
from django.shortcuts import get_object_or_404, render
from .models import Category, Product

# Index View (No changes)

def index(request):
    cat_list = Category.objects.all().order_by('id')[:10]  # Fetch categories
    return render(request, 'myapp/index.html', {'cat_list': cat_list})

    # response = HttpResponse()
    # response.write("<h2>List of Categories:</h2>")
    # for category in cat_list:
    #     response.write(f"<p>{category.id}: {category.name}</p>")
    #
    # response.write("<h2>Top 5 Most Expensive Products:</h2>")
    # for product in product_list:
    #     response.write(f"<p>{product.name} - ${product.price}</p>")
    #
    # return response

# About View (Restored to its original version)
# def about(request):
#      return render(request, 'myapp/about0.html')
def about(request):
    return render(request, 'myapp/about.html')

# Category Detail View - Improved formatting
# def detail(request, cat_no):
#      category = get_object_or_404(Category, id=cat_no)
#      return render(request, 'myapp/detail.html', {'category': category})

def detail(request, cat_no):
    category = get_object_or_404(Category, id=cat_no)
    return render(request, 'myapp/detail.html', {'category': category})