from django.http import HttpResponse
from django.shortcuts import get_object_or_404
from .models import Category, Product

# Index View (No changes)
def index(request):
    cat_list = Category.objects.all().order_by('id')[:10]  # Get up to 10 categories
    product_list = Product.objects.all().order_by('-price')[:5]  # Get top 5 expensive products

    response = HttpResponse()
    response.write("<h2>List of Categories:</h2>")
    for category in cat_list:
        response.write(f"<p>{category.id}: {category.name}</p>")

    response.write("<h2>Top 5 Most Expensive Products:</h2>")
    for product in product_list:
        response.write(f"<p>{product.name} - ${product.price}</p>")

    return response

# About View (Restored to its original version)
def about(request):
    return HttpResponse("This is an Online Store APP.")

# Category Detail View - Improved formatting
def detail(request, cat_no):
    category = get_object_or_404(Category, id=cat_no)
    products = Product.objects.filter(category=category)

    response = HttpResponse()
    response.write(f"<h1>Category: {category.name}</h1>")

    # Use 'warehouse' field if it exists, otherwise show default text
    warehouse_info = getattr(category, 'warehouse', 'No warehouse information available')
    response.write(f"<h2>Warehouse Location: {warehouse_info}</h2>")

    response.write(f"<h3>Total Products in this Category: {products.count()}</h3>")

    response.write("<h3>Products Available:</h3>")
    if products.exists():
        response.write("<ul>")
        for product in products:
            response.write(f"<li><strong>{product.name}</strong> - ${product.price}, Stock: {product.stock}</li>")
        response.write("</ul>")
    else:
        response.write("<p>No products available in this category.</p>")

    return response