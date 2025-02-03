from django.http import HttpResponse
from django.shortcuts import get_object_or_404
from .models import Category, Product


# Index View: Displays up to 10 categories and 5 products sorted by price
def index(request):
    cat_list = Category.objects.all().order_by('id')[:10]
    product_list = Product.objects.all().order_by('-price')[:5]  # Most expensive first

    response = HttpResponse()
    response.write("<p>List of Categories:</p>")
    for category in cat_list:
        response.write(f"<p>{category.id}: {category.name}</p>")

    response.write("<p>Top 5 Products:</p>")
    for product in product_list:
        response.write(f"<p>{product.name} - ${product.price}</p>")

    return response


# About View: Displays a simple message
def about(request):
    return HttpResponse("This is an Online Store APP.")


# Detail View: Displays warehouse location and products for a given category
def detail(request, cat_no):
    category = get_object_or_404(Category, id=cat_no)
    products = Product.objects.filter(category=category)

    response = HttpResponse()
    response.write(f"<p>Warehouse Location: {category.warehouse_location}</p>")
    response.write("<p>Products in this Category:</p>")

    for product in products:
        response.write(f"<p>{product.name} - ${product.price}</p>")

    return response