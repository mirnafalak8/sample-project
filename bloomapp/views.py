from django.shortcuts import get_object_or_404, redirect, render
from bloomapp.models import Cart, Category, Contact, Order, OrderItem, Product, UserProfile, Wishlist
from django.contrib.auth.models import User,auth
from django.contrib.auth import authenticate, login
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.db.models import Q
from django.http import JsonResponse
from django.core.mail import send_mail
from django.conf import settings
import random
import string

# Create your views here.
def home(request):
    categories = Category.objects.all()
    user = request.user.id
    carts = Cart.objects.filter(user=user)
    total_quantity = sum(cart.quantity for cart in carts)
    return render(request, 'home.html', {'total_quantity': total_quantity, 'categories': categories})

def signup(request):
    return render(request,'signup.html')

def signin_page(request):
    return render(request,'signin.html')

def about_us(request):
    categories = Category.objects.all()
    return render(request,'about.html',{'categories': categories})

def product_search(request):
    if request.method == 'GET':
        search = request.GET.get('search')
        products = Product.objects.filter(Q(name__icontains=search) | Q(category__name__icontains=search))
        return render(request, 'search_results.html', {'products': products})
    else:
        return render(request, 'search_results.html')
    
def contact_view(request):
    if request.method == 'POST':
        name = request.POST['name']
        email = request.POST['email']
        message = request.POST['message']
        contact = Contact(name=name, email=email, message=message)
        contact.save()
        return redirect('home')
    categories = Category.objects.all()
    return render(request, 'contact.html',{'categories': categories})

def ad_contact(request):
    contacts = Contact.objects.all()
    categories = Category.objects.all()
    return render(request, 'ad_contact.html', {'contacts': contacts,'categories': categories})

def usercreate(request):
    if request.method == 'POST':
        first_name = request.POST['first_name']
        last_name = request.POST['last_name']
        address = request.POST['address']
        phone = request.POST['phone']
        username = request.POST['username']
        email = request.POST['email']
        # password_length = 8
        # characters = string.ascii_letters + string.digits
        # password = ''.join(random.choice(characters) for _ in range(password_length))
        password = request.POST['password']
        if len(password) < 8:
            messages.error(request, 'Password must be at least 8 characters long.')
            return redirect('signup')
        if not any(char.isupper() for char in password):
            messages.error(request, 'Password must contain at least one uppercase letter.')
            return redirect('signup')
        if not any(char.isdigit() for char in password):
            messages.error(request, 'Password must contain at least one numeric digit.')
            return redirect('signup')
        if not any(char in string.punctuation for char in password):
            messages.error(request, 'Password must contain at least one special character.')
            return redirect('signup')
        if User.objects.filter(username=username).exists():
            messages.info(request, 'This username already exists!')
            return redirect('signup')
        elif User.objects.filter(email=email).exists():
            messages.info(request, 'This email address already exists!')
            return redirect('signup')
        else:
            user = User.objects.create_user(
                first_name=first_name,
                last_name=last_name,
                username=username,
                password=password,
                email=email
            )
            user_profile = UserProfile.objects.create(
                user=user,
                phone_number=phone,
                address=address
            )
            send_mail(
                'Welcome to our InBloom Website',
                f'Username: {username}\nPassword: {password}',
                'mirnafalak@gmail.com',
                recipient_list=[email],
                fail_silently=False,
            )
            messages.success(request, 'Your account has been created successfully!')
            return redirect('signin_page')
    else:
        return redirect('signin_page')
    
def signin(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = auth.authenticate(username=username, password=password)
        if user is not None:
            if user.is_staff:
                login(request,user)
                return redirect('admin_home_page')
            else:
                login(request,user)
                auth.login(request,user)
                # return redirect('user_home_page')
                return redirect('home')
        else:
            return redirect('signin_page')
    return redirect('signin_page')

@login_required(login_url='signin')
def admin_home_page(request):
    categories = Category.objects.all()
    return render(request, 'adminhome.html',{'categories': categories})

def logout(request):
	auth.logout(request)
	return redirect('home')

def category_page(request):
    if request.method == 'POST':
        name = request.POST.get('name')
        data = Category(name=name)
        data.save()
        return redirect('category_page')
    categories = Category.objects.all()
    return render(request, 'category.html', {'categories': categories})

def categories(request, category_name):
    categories = Category.objects.all()
    category = get_object_or_404(Category, name=category_name)
    products = Product.objects.filter(category=category)
    context = {'category_name': category_name, 'products': products,'categories':categories}
    return render(request, 'category_page.html', context)

def fashion_categories_view(request, category_names):
    categories = Category.objects.all()
    category_list = category_names.split(',')
    categories_to_display = ['Ladies', 'Gents', 'Kids']  
    filtered_categories = [category for category in category_list if category in categories_to_display]
    products = Product.objects.filter(category__name__in=filtered_categories)
    return render(request, 'fashion_categories.html', {'category_list': filtered_categories, 'products': products,'categories':categories})

def electronics_categories_view(request, category_names):
    categories = Category.objects.all()
    category_list = category_names.split(',')
    categories_to_display = ['laptop', 'mobile']  
    filtered_categories = [category for category in category_list if category in categories_to_display]
    products = Product.objects.filter(category__name__in=filtered_categories)
    return render(request, 'electronics_categories.html', {'category_list': filtered_categories, 'products': products,'categories':categories})

def appliances_categories_view(request, category_names):
    categories = Category.objects.all()
    category_list = category_names.split(',')
    categories_to_display = ['AC', 'microwaves','washing machine','Refrigerators']  
    filtered_categories = [category for category in category_list if category in categories_to_display]
    products = Product.objects.filter(category__name__in=filtered_categories)
    return render(request, 'appliances_categories.html', {'category_list': filtered_categories, 'products': products,'categories':categories})

def productpage(request):
    if request.method == 'POST':
        name = request.POST['name']
        description = request.POST['description']
        price = request.POST['price']
        photo = request.FILES.get('file')
        select = request.POST['select']
        category = Category.objects.get(id=select)
        product = Product(name=name, category=category, description=description, price=price, image=photo)
        product.save() 
        return redirect('productpage')
    categories = Category.objects.all()
    product_detail = Product.objects.all()
    return render(request, 'ad_product.html', {'categories': categories, 'product': product_detail})

def p_editpage(request,pk):
    edit = Product.objects.get(id=pk)
    categories = Category.objects.all()
    context = {'categories': categories}
    return render(request,'edit_product.html',{'product':edit},context)

def p_edit_form(request,pk):
    if request.method == 'POST':
        product = Product.objects.get(id=pk)
        product.name = request.POST.get('name')
        product.description = request.POST.get('description', '')
        # product.description = request.POST.get('description')
        product.price = request.POST.get('price')
        select=request.POST.get('select')
        category=Category.objects.get(id=select)
        product.category = category
        old=product.image
        new=request.FILES.get('file')
        if old !=None and new==None:
            product.image=old
        else:
            product.image=new
        product.save()
        return redirect('admin_home_page')
    product = Product.objects.get(id=pk)
    categories = Category.objects.all()
    return render(request,'edit_product.html',{'product':product,'categories': categories})

def p_delete_form(request,pk):
    edit=Product.objects.get(id=pk)
    edit.delete()
    return redirect('admin_home_page')

def UserDetails(request):
    user_detail = UserProfile.objects.all()
    categories = Category.objects.all()
    return render(request,'ad_user.html',{'users':user_detail,'categories':categories})

def ad_useredit(request,pk):
    edit = UserProfile.objects.get(id=pk)
    return render(request,'edit_user.html',{'user':edit})

def ad_userform(request,pk):
    if request.method == 'POST':
        edit = UserProfile.objects.get(id=pk)
        user = edit.user
        user.first_name = request.POST.get('first_name')
        user.last_name = request.POST.get('last_name')
        edit.phone_number = request.POST.get('phone')
        user.email = request.POST.get('email')
        edit.address = request.POST.get('address')
        edit.user.username = request.POST.get('username')
        edit.save()
        user.save()
        return redirect('UserDetails')
    edit = UserProfile.objects.get(id=pk)
    return render(request,'edit_user.html',{'user':edit})

def ad_userdelete(request,pk):
    edit= UserProfile.objects.get(id=pk)
    edit.delete()
    return redirect('UserDetails')

def allproducts(request):
    products = Product.objects.all()
    categories = Category.objects.all()
    # wishlist = Wishlist.objects.filter(user=request.user).first()
    return render(request, 'allproducts.html', {'products': products, 'categories': categories})

def product_detail(request, pk):
    product = Product.objects.get(pk=pk)
    return render(request, 'product_detail.html', {'product': product})

@login_required(login_url='signin')
def cart(request):
    carts = Cart.objects.filter(user=request.user)
    total_price = 0
    grand_total = sum(cart.product.price * cart.quantity for cart in carts)

    for cart in carts:
        subtotal = cart.product.price * cart.quantity
        total_price += subtotal
        cart.subtotal = subtotal
        # total_quantity += cart.quantity

    return render(request, 'cart.html', {'carts': carts, 'total_price': total_price,'grand_total': grand_total})

@login_required(login_url='signin')
def add_to_cart(request, pk):
    product = Product.objects.filter(id=pk).first()
    if product:
        try:
            cart = Cart.objects.get(user=request.user, product=product)
            cart.quantity += 1
            cart.save()
        except Cart.DoesNotExist:
            cart = Cart(user=request.user, product=product)
            cart.save()
    return redirect('cart')

@login_required(login_url='signin')
def remove_from_cart(request, pk):
    cart = Cart.objects.filter(id=pk, user=request.user).first()
    if cart:
        cart.delete()
    return redirect('cart')

@login_required(login_url='signin')
def update_cart(request,pk):
    cart = Cart.objects.filter(id=pk, user=request.user).first()
    if cart and request.method == 'POST':
        quantity = int(request.POST.get('quantity', 1))
        cart.quantity = quantity
        cart.save()
    return redirect('cart')

def place_order_page(request):
    return render(request, 'place_order.html')

def place_order(request):
    if request.method == 'POST':
        address = request.POST.get('address')
        city = request.POST.get('city')
        state = request.POST.get('state')
        postal_code = request.POST.get('postal_code')
        card_number = request.POST.get('card_number')
        card_holder_name = request.POST.get('card_holder_name')
        expiration_date = request.POST.get('expiration_date')
        cvv = request.POST.get('cvv')
        request.session['order_placed'] = True
        return redirect('order_success')
    return render(request, 'place_order.html')

@login_required(login_url='signin')
def order_success(request):
    categories = Category.objects.all()
    return render(request, 'order_success.html',{'categories':categories})

@login_required(login_url='signin')
def ordered_items(request):
    if request.method == 'POST':  
        order = Order.objects.create(user=request.user)
        cart_items = Cart.objects.filter(user=request.user)
        for cart_item in cart_items:
            OrderItem.objects.create(order=order, product=cart_item.product, quantity=cart_item.quantity)
        cart_items.delete()
    ordered_items = OrderItem.objects.filter(order__user=request.user)
    for ordered_item in ordered_items:
        ordered_item.total_price = ordered_item.quantity * ordered_item.product.price
        ordered_item.disable_button = False  
        if ordered_item.order.status == 'confirmed' and ordered_item.product.is_confirmed_by_admin:
            ordered_item.disable_button = True 
    
    context = {
        'ordered_items': ordered_items,
        'order_placed': request.session.get('order_placed', False)
    }
    return render(request, 'ordered_item.html', context)

def update_order_status(request, ordered_item_id):
    ordered_item = OrderItem.objects.get(id=ordered_item_id)
    ordered_item.order.status = 'O'  # Set the status to 'O' (Ordered)
    ordered_item.order.save()
    return JsonResponse({'message': 'Order status updated successfully.'})

def user_ordered_items(request):
    order_items = OrderItem.objects.select_related('order__user', 'product').all()
    categories = Category.objects.all()
    context = {'order_items': order_items,'categories':categories}
    return render(request, 'user_ordered_items.html', context)

@login_required(login_url='signin')
def confirm_order(request, order_id):
    if request.method == 'POST':
        order = Order.objects.get(id=order_id)
        order.status = 'C'
        order.is_confirmed = True
        order.save()
    return redirect('user_ordered_items')

@login_required(login_url='signin')
def cancel_order(request, order_id):
    if request.method == 'POST':
        order = Order.objects.get(id=order_id)
        order.status = 'X'
        order.is_cancelled = True
        order.save()
    return redirect('user_ordered_items')

@login_required(login_url='signin')
def wishlist(request):
    user = request.user
    wishlist_items = Wishlist.objects.filter(user=user)
    categories = Category.objects.all()
    context = {'wishlist_items': wishlist_items,'categories':categories}
    return render(request, 'wishlist.html', context)

@login_required(login_url='signin')
def add_to_wishlist(request, pk):
    if request.method == 'POST':
        user = request.user
        Wishlist.objects.create(user=user, product_id=pk)
        return redirect('wishlist')
    else:
        return redirect('wishlist')

@login_required(login_url='signin')
def remove_from_wishlist(request, pk):
    wishlist_item = Wishlist.objects.get(id=pk)
    wishlist_item.delete()
    return redirect('wishlist')
