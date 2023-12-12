from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.views import PasswordChangeView, PasswordChangeDoneView
from django.urls import reverse_lazy
from django.utils import timezone

from rest_framework.authtoken.models import Token

from .models import Product, Review, Category
from .forms import RegistrationForm, LoginForm, ReviewForm


@login_required(login_url='custom_login')
def products(request):
    products = Product.objects.all()

    category_id = request.GET.get('category', None)
    sort_by = request.GET.get('sort_by', 'name')

    if category_id and category_id != '0':
        products = products.filter(category__id=category_id)

    products = products.order_by(sort_by)

    categories = Category.objects.all()

    context = {
        'products': products,
        'categories': categories,
        'selected_category': int(category_id) if category_id else None,
        'selected_sort': sort_by,
    }

    return render(request, 'products.html', context)


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
#         order = Order.objects.create(
#             user=request.user,
#             total_price=product.price
#         )
#         order.products.add(product)


#         return redirect('buy_success')

#     return render(request, 'buy_product.html', {'product': product})


def detail_product(request, product_id):
    product = get_object_or_404(Product, pk=product_id)

    return render(request, 'detail_product.html', {'product': product})


def buy_success(request, product_id):
    return render(request, 'buy_success.html', {'product_id': product_id})

# def write_review(request, product_id):
#     product = get_object_or_404(Product, pk=product_id)

#     return render(request, 'write_review.html', {'product': product})    

def custom_login(request):
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            user = authenticate(request, username=username, password=password)

            if user is not None:
                login(request, user)

                # Create or get the token for the user
                token, created = Token.objects.get_or_create(user=user)

                # You can store the token in the session if needed
                request.session['auth_token'] = token.key

                return redirect('products')
            else:
                form.add_error(None, 'Invalid credentials. Please try again.')

    else:
        form = LoginForm()

    return render(request, 'login.html', {'form': form})


def custom_logout(request):
    logout(request)
    return redirect('custom_login')


class CustomPasswordChangeView(PasswordChangeView):
    template_name = 'password_change_form.html'
    success_url = reverse_lazy('password_change_done')

    def form_valid(self, form):
        response = super().form_valid(form)
        logout(self.request)
        return response

class CustomPasswordChangeDoneView(PasswordChangeDoneView):
    template_name = 'password_change_done.html'

    def get(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            # If the user is authenticated, redirect to a different URL
            return super().get(request, *args, **kwargs)
        else:
            # If the user is not authenticated, redirect to the login page
            logout(request)
            return redirect(reverse_lazy('custom_login'))


@login_required(login_url='custom_login')
def write_review(request, product_id):
    product = Product.objects.get(pk=product_id)

    if request.method == 'POST':
        form = ReviewForm(request.POST)
        if form.is_valid():
            review = form.save(commit=False)
            review.product = product
            review.user = request.user
            review.save()
            return redirect('review_success')
    else:
        form = ReviewForm()

    reviews = Review.objects.filter(product=product)

    # Convert UTC time to IST
    for review in reviews:
        review.created_at = review.created_at.astimezone(timezone.get_current_timezone())

    context = {
        'form': form,
        'product': product,
        'reviews': reviews,
    }

    return render(request, 'write_review.html', context)


@login_required(login_url='custom_login')
def review_success(request):
    messages.success(request, 'Review submitted successfully!')
    return redirect('products')
