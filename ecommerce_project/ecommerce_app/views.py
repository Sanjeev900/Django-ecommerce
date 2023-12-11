from django.shortcuts import render, redirect, get_object_or_404
from .models import Product, Order
from .forms import RegistrationForm
from django.contrib import messages
from django.contrib.auth.decorators import login_required


def products(request):
    products = Product.objects.all()

    return render(request, 'products.html', {'products': products})

def product_detail(request, product_id):
    product = Product.objects.get(id=product_id)
    return render(request, 'product_detail.html', {'product': product})

def register(request):
    if request.method == 'POST':
        form = RegistrationForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Account created successfully. You can now log in.')
            return redirect('registration_success')
    else:
        form = RegistrationForm()

    return render(request, 'register.html', {'form': form})


def registration_success(request):
    return render(request, 'registration_success.html')


# @login_required
# def buy_product(request, product_id):
#     product = get_object_or_404(Product, pk=product_id)

#     if request.method == 'POST':
#         # Your logic to handle buying a product goes here
#         # For example, create an order for the current user and the selected product
#         order = Order.objects.create(
#             user=request.user,
#             total_price=product.price
#         )
#         order.products.add(product)

#         # You can customize the logic for calculating the total price and adding multiple products

#         # Redirect to a success page or any other page as needed
#         return redirect('buy_success')

#     return render(request, 'buy_product.html', {'product': product})


def buy_product(request, product_id):
    product = get_object_or_404(Product, pk=product_id)

    return render(request, 'buy_product.html', {'product': product})


def buy_success(request):
    return render(request, 'buy_success.html')

def write_review(request, product_id):
    # Your logic to handle writing a review goes here
    product = get_object_or_404(Product, pk=product_id)

    # Example: Display a simple form to submit a review
    return render(request, 'write_review.html', {'product': product})    