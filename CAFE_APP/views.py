from django.http import Http404, HttpResponse
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from .models import Cart
from django.conf import settings
from datetime import datetime, timedelta
from django.contrib import messages
import re
from django.utils import timezone
from .models import *
from datetime import date


# Create your views here.

def index(request):
    data = Food_items.objects.all()
    blogs = Blog.objects.all()
    return render(request, 'index.html', locals())


@login_required
def user_home(request):
    notification_count = Notifications.objects.filter(user_id=request.user.id, read=False).count()
    count = Cart.objects.filter(user_id=request.user.id).count()
    data = Food_items.objects.all()
    return render(request, 'user_home.html', locals())


def about(request):
    notification_count = Notifications.objects.filter(user_id=request.user.id, read=False).count()
    count = Cart.objects.filter(user_id=request.user.id).count()
    return render(request, 'about.html',locals())

def blog(request):
    if request.user.is_authenticated:
        logout(request)
        # Admin logout
        request.session.flush()
    blogs = Blog.objects.all()
    return render(request, 'blog.html', locals())

def blog_read(request, id):
    blogs = Blog.objects.filter(id=id)
    return render(request, 'blog_read.html', locals())

def contact(request):
    notification_count = Notifications.objects.filter(user_id=request.user.id, read=False).count()
    count = Cart.objects.filter(user_id=request.user.id).count()
    if request.method == "POST":
        name = request.POST.get('name')
        email = request.POST.get('email')
        phone = request.POST.get('phone')
        subject = request.POST.get('subject')
        message = request.POST.get('message')
        created_at = request.POST.get('created_at')
        contacts = Contact.objects.create(name=name,
                                          email=email,
                                          phone=phone,
                                          subject=subject,
                                          message=message,
                                          created_at=created_at
                                          )
        return redirect('index')
    return render(request, 'contact.html', locals())


def login_page(request):
    return render(request, 'login.html')


def cofe_read(request,id):
    data = Food_items.objects.filter(id=id)
    return render(request, 'cofe_read.html', locals())


def Registration(request):
    if request.method == 'POST':
        name = request.POST.get('name')
        email = request.POST.get('email')
        phone_number = request.POST.get('phone')
        password = request.POST.get('password')
        try:
            User.objects.get(username=email)
            return render(request, 'login.html')
        except User.DoesNotExist:
            user = User.objects.create(
                name=name,
                email=email,
                username=email,
                phone_number=phone_number,
                is_superuser=0,
                is_staff=0,
                user_type=3
            )
            user.set_password(password)
            user.save()
            return render(request, 'login.html')
    else:
        return render(request, 'login.html')


def login_function(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        password = request.POST.get('password')
        user = authenticate(username=email, password=password)
        if user is not None:
            if user.is_superuser:
                login(request, user)
                if user.user_type == 1:
                    request.session['is_admin'] = True
                    return redirect(Dashboard)

            else:

                login(request, user)
                if user.user_type==3:
                    request.session['is_admin'] = False

                    return redirect(user_home)
        else:
            return render(request, 'login.html')
    else:
        return render(request, 'login.html')

def forgot_password(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        password = request.POST.get('password')
        user = User.objects.get(username=email)
        if user is not None:
            user.set_password(password)
            user.save()
            messages.add_message(request, messages.SUCCESS, "Password Changed Successfully.")
        return render(request, 'login.html')
    else:
        return render(request,'forgot_password.html')
        
    

@login_required
def logout_function(request):
    logout(request)
    return redirect(index)


#------------- admin module ----------------------------
@login_required
def Dashboard(request):
    food_count = Food_items.objects.all().count()
    blog_count = Blog.objects.all().count()
    notification_count = Notifications.objects.all().count()
    user_count = User.objects.all().count()
    order_count = Orders.objects.all().count()
    new_order = Orders.objects.filter(order_time__date=date.today()).order_by('-order_time')[:5]
    return render(request, 'dashboard.html', locals())

def admin_blog(request):
    blogs = Blog.objects.all()
    return render(request, 'admin_blog.html', locals())

def admin_view_blog(request, id):
    blog = Blog.objects.get(id=id)
    return render(request,'admin_view_blog.html',locals())

def add_blog(request):
    if request.method == 'POST':
        title = request.POST.get('title')
        date = request.POST.get('date')
        description = request.POST.get('description')
        image = request.FILES.get('image')
        try:
            Blog.objects.get(id=id)
            messages.add_message(request, messages.WARNING, "Blog already exist.")
        except:
            blogs = Blog.objects.create(title=title,
                                        date=date,
                                        description=description,
                                        image=image
                                        )

            blogs.save()
            msg = "New Item Added Successfully,Itemcode : {}".format(id)
            messages.add_message(request, messages.SUCCESS, msg)
            blogs = Blog.objects.all()
        return render(request, 'admin_blog.html', locals())
    return render(request, 'add_blog.html')


def edit_blog(request, id):
    blog = Blog.objects.get(id=id)
    if request.method == "POST":
        blog.title = request.POST.get('title')
        blog.date = request.POST.get('date')
        blog.description = request.POST.get('description')
        blog.image = request.FILES.get('Image')
        blog.save()
        return redirect(admin_blog)
    else:
        blogs = Blog.objects.filter(id=id)
    return render(request, 'edit_blog.html', locals())

def delete_blog(request, id):
    Blog.objects.filter(id=id).delete()
    msg = "Blog Deleted Successfully"
    messages.add_message(request, messages.SUCCESS, msg)
    blogs = Blog.objects.all()
    return render(request, 'admin_blog.html', locals())

def admin_contact(request):
    contacts = Contact.objects.all()
    print(contacts)
    return render(request, 'admin_contact.html',{'contacts':contacts})




@login_required
def admin_products(request):
    try:
        data = Food_items.objects.all()
        return render(request, 'admin_products.html', locals())
    except:
        text = "No data found"
        return render(request, 'admin_products.html', locals())

@login_required
def admin_view_product(request, id):
    try:
        data = Food_items.objects.filter(id=id)
        return render(request, 'admin_view_product.html', locals())
    except:
        text = "No data found"
        return render(request, 'admin_products.html', {'text': text})

@login_required
def add_item(request):
    if request.method == 'POST':
        item_name = request.POST.get('item_name')
        item_id = request.POST.get('item_id')
        description = request.POST.get('description')
        price = request.POST.get('price')
        image = request.FILES.get('image')
        try:
            Food_items.objects.get(item_id=item_id)
            messages.add_message(request, messages.WARNING, "Item already exist.")
            data = Food_items.objects.all()
            return render(request, 'admin_products.html', locals())
        except:
            data = Food_items.objects.create(item_name=item_name,
                                             item_id=item_id,
                                             description=description,
                                             price=price,
                                             image=image
                                             )

            data.save()
            msg = "New Item Added Successfully,Itemcode : {}".format(item_id)
            messages.add_message(request, messages.SUCCESS, msg)
            data = Food_items.objects.all()
            return render(request, 'admin_products.html', locals())


    else:
        return render(request, 'add_item.html')

@login_required
def edit_item(request, id):
    if request.method == "POST":
        item_name = request.POST.get('item_name')
        item_id = request.POST.get('item_id')
        description = request.POST.get('description')
        price = request.POST.get('price')
        image = request.FILES.get('Image')
        Food_items.objects.filter(id=id).update(item_name=item_name,
                                                item_id=item_id,
                                                description=description,
                                                price=price
                                                )
        instance = get_object_or_404(Food_items, id=id)
        if image:
            instance.image = image
        instance.save()
        return redirect(admin_view_product, id)
    else:
        data = Food_items.objects.filter(id=id)
        return render(request, 'edit_item.html', locals())

@login_required
def delete_item(request, id):
    Food_items.objects.filter(id=id).delete()
    msg = "Item Deleted Successfully"
    messages.add_message(request, messages.SUCCESS, msg)
    data = Food_items.objects.all()
    return render(request, 'admin_products.html', locals())

@login_required
def admin_orders(request):
    coffee_details = Food_items.objects.all()
    new_orders = Orders.objects.filter(status=1).order_by('-order_time')
    accepted_orders = Orders.objects.filter(status=2).order_by('-order_time')
    delivered_orders = Orders.objects.filter(status=3).order_by('-order_time')
    cancel_order = Orders.objects.filter(status=4).order_by('-order_time')

    # for i in all_orders:
    #     for j in coffee_details:
    #         if i.item_id == j.id:
    #             print(i.item_id,j.id)

    return render(request, 'admin_orders.html', locals())


@login_required
def Accept_item(request, id):
    Orders.objects.filter(id=id).update(status=2)
    current_order = Orders.objects.filter(id=id).first()

    user_id = User.objects.filter(id=current_order.user_id_id).first()

    food_items = Food_items.objects.filter(orders=current_order)
    item_name = ", ".join([food.item_name for food in food_items])
    message1 = f"Your order  has been accepted."
    Notifications.objects.create(user_id=user_id, read=False, message=message1)

    return redirect(admin_orders)


@login_required
def Pending_item(request, id):
    Orders.objects.filter(id=id).update(status=3)
    current_order = Orders.objects.filter(id=id).first()
    user_id = User.objects.filter(id=current_order.user_id_id).first()
    message1 =f"Your order has been arrived."
    Notifications.objects.create(user_id=user_id, read=False, message=message1)

    return redirect(admin_orders)


@login_required
def Cancel_item(request, id):
    Orders.objects.filter(id=id).update(status=4)
    current_order = Orders.objects.filter(id=id).first()
    user_id = User.objects.filter(id=current_order.user_id_id).first()
    message1 = f"Your order has been cancelled."
    Notifications.objects.create(user_id=user_id, read=False, message=message1)

    return redirect(admin_orders)

@login_required
def notification_admin(request):
    user = User.objects.get(is_superuser=1)
    count = Notifications.objects.filter(id=user.id, read=False).count()
    notification = Notifications.objects.filter(user_id=request.user.id).order_by('-datetime')
    current_time = datetime.now()

    for i in notification:
        current_time = datetime.now()
        time_difference = current_time - i.datetime
        total_seconds = int(time_difference.total_seconds())

        if total_seconds < 60:
            i.time_ago = f"{total_seconds} seconds ago"
        elif total_seconds < 3600:
            i.time_ago = f"{total_seconds // 60} minutes ago"
        elif total_seconds < 86400:  # Less than 24 hours
            i.time_ago = f"{total_seconds // 3600} hours ago"
        elif total_seconds < 172800:  # Less than 48 hours (1 day)
            i.time_ago = "1 day ago"
        elif total_seconds < 604800:  # Less than a week
            i.time_ago = f"{total_seconds // 86400} days ago"
        elif total_seconds < 1209600:  # Less than 2 weeks (1 week)
            i.time_ago = "1 week ago"
        else:
            weeks = total_seconds // 604800
            i.time_ago = f"{weeks} weeks ago"

    for i in notification:
        i.read = True
        i.save()
    return render(request, 'notification_admin.html', locals())

@login_required
def admin_users(request):
    user_id = User.objects.filter(user_type=3)
    return render(request, 'admin_users.html', locals())



#--------------------user module-------------------------

def coffees(request):
    notification_count = Notifications.objects.filter(user_id=request.user.id, read=False).count()
    count = Cart.objects.filter(user_id=request.user.id).count()
    data = Food_items.objects.all()
    return render(request, 'coffees.html', locals())

@login_required
def add_to_cart(request, id):
    notification_count = Notifications.objects.filter(user_id=request.user.id, read=False).count()
    count = Cart.objects.filter(user_id=request.user.id).count()
    try:
        Cart.objects.get(item_id=id)
        data = Cart.objects.filter(item_id=id, user_id=request.user.id)
        food_details = Food_items.objects.all()
        for i in data:
            for j in food_details:
                if j.id == i.item_id:
                    quantity = i.quantity
                    price = j.price
        quantity += 1
        item_total = quantity * price
        print(quantity, price, item_total)
        Cart.objects.filter(item_id=id, user_id=request.user.id).update(quantity=quantity, item_total=item_total)

        return redirect(coffees)
    except:
        data = Food_items.objects.get(id=id)
        user = request.user
        price = data.price
        quantity = 1
        total = price * quantity
        cart = Cart.objects.create(item_id=id, user_id=user, quantity=quantity, item_total=total)
        cart.save()
        return redirect(coffees)


@login_required
def increment_quantity(request, item_id):
    items = Cart.objects.filter(item=item_id)
    if not items.exists():
        raise Http404("No cart item found.")

    for item in items:
        item.quantity += 1
        item.save()

    return redirect(cart_item)

@login_required
def decrement_quantity(request, item_id):
    items = Cart.objects.filter(item=item_id)

    if not items.exists():
        raise Http404("No cart item found.")

    for item in items:
        if item.quantity > 1:
            item.quantity -= 1
            item.save()
        else:
            item.delete()  # Remove item if quantity reaches 0

    return redirect(cart_item)

@login_required
def cart_item(request):
    notification_count = Notifications.objects.filter(user_id=request.user.id, read=False).count()
    cart_data = Cart.objects.filter(user_id=request.user)
    address = Address.objects.filter(user_id=request.user)
    # print(cart_data)
    coffee_details = Food_items.objects.all()

    # for i in cart_data:
    #     # print(i)
    #     for j in coffee_details:
    #         if j.id == i.item_id_id:
    #             print(j.item_name)
    grand_total = 0
    quantity = 0
    for i in cart_data:
        grand_total += i.item_total
    count = Cart.objects.filter(user_id=request.user.id).count()
    return render(request,'cart_item.html', locals())


@login_required
def delete_cart_item(request, id):
    cart_items = Cart.objects.filter(item_id=id)
    cart_items.delete()
    return redirect(cart_item)


@login_required
def empty_cart(request):
    Cart.objects.filter(user_id=request.user).delete()
    return redirect(cart_item)

# import uuid

# Generate a unique order ID
# unique_order_id = str(uuid.uuid4())


import random
from datetime import datetime


@login_required
def order_items(request):
    notification_count = Notifications.objects.filter(user_id=request.user.id, read=False).count()
    count = Cart.objects.filter(user_id=request.user.id).count()
    if request.method=="POST":

        address=request.POST.get("address")

        address=Address.objects.get(id=address)
        print(address)
        data = request.user
        cart_data = Cart.objects.filter(user_id=request.user)
        coffee_details = Food_items.objects.all()
        user = User.objects.get(id=request.user.id)
        x = datetime.now()
        ordered_time = x
        grand_total = 0
        orders_list = []
        for i in cart_data:
            grand_total += i.item_total

        for i in cart_data:
            for j in coffee_details:
                if i.item_id == j.id:
                    item = Food_items.objects.get(id=i.item_id)
                    # Generate a unique 6-digit order ID
                    while True:
                        unique_order_id = random.randint(100000, 999999)  # 6-digit number
                        if not Orders.objects.filter(order_id=unique_order_id).exists():
                            break

                    my_orders = Orders.objects.create(
                        user_id=user,
                        item=item,
                        quantity=i.quantity,
                        order_time=x,
                        total_price=i.item_total,
                        order_id=unique_order_id,
                        status=1,
                        address=address

                    )
                    my_orders.save()
                    # print(my_orders.order_id)
                    orders_list.append(my_orders.order_id)

        print(orders_list)
        text_to_admin = "New Order placed with order id "+','.join(map(str, orders_list))
        text_user = User.objects.get(is_superuser=1)
        notify = Notifications.objects.create(user_id=text_user,
                                              message=text_to_admin,
                                              read=0
                                              )
        notify.save()

        text_to_user = "Your Order has been placed track your order id:" +','.join(map(str, orders_list))
        notify1 = Notifications.objects.create(user_id=user,
                                               message=text_to_user,
                                               read=0
                                               )
        notify1.save()
        return render(request, 'invoice.html', locals())
    return redirect(cart_item)

def profile(request):
    notification_count = Notifications.objects.filter(user_id=request.user.id, read=False).count()
    count = Cart.objects.filter(user_id=request.user.id).count()
    user = request.user

    address = Address.objects.filter(user_id=user)
    print(address)

    return render(request, 'profile.html', locals())

@login_required
def add_address(request):
    notification_count = Notifications.objects.filter(user_id=request.user.id, read=False).count()
    count = Cart.objects.filter(user_id=request.user.id).count()
    user_data = request.user

    if request.method == 'POST':
            address = request.POST.get('address')
            city = request.POST.get('city')
            Zipcode = request.POST.get('Zipcode')
            Land_Mark = request.POST.get('Land_Mark')
            phone_number = request.POST.get('phone_number')
            data = Address.objects.create(address=address,
                                          city=city,
                                          Zipcode=Zipcode,
                                          Land_Mark=Land_Mark,
                                          user_id=user_data,
                                          phone_number=phone_number
                                          )
            return redirect('profile')
    return render(request,'add_address.html', locals())


def get_address(request, id):
    notification_count = Notifications.objects.filter(user_id=request.user.id, read=False).count()
    count = Cart.objects.filter(user_id=request.user.id).count()
    address=Address.objects.get(id=id)
    return render(request, 'change_address.html', locals())


@login_required
def change_address(request, id):
    notification_count = Notifications.objects.filter(user_id=request.user.id, read=False).count()
    count = Cart.objects.filter(user_id=request.user.id).count()
    user_data = User.objects.get(id=request.user.id)
    address=Address.objects.get(id=id)
    if request.method == 'POST':
        address.address = request.POST.get('address')
        address.city = request.POST.get('city')
        address.phone_number = request.POST.get('phone_number')
        address.Zipcode = request.POST.get('Zipcode')
        address.Land_Mark = request.POST.get('Land_Mark')
        address.save()
    return redirect('profile',locals())


def delete_address(request, id):
    address = get_object_or_404(Address, id=id)
    address.delete()
    messages.success(request, "Address deleted successfully.")
    return redirect('profile')


@login_required
def user_notification(request):
    notification_count = Notifications.objects.filter(user_id=request.user.id, read=False).count()
    notification = Notifications.objects.filter(user_id=request.user.id).order_by('-id')

    current_time = datetime.now()

    count = Cart.objects.filter(user_id=request.user.id).count()
    orders = Orders.objects.filter(id=request.user.id)


    for i in notification:
        current_time = datetime.now()
        time_difference = current_time - i.datetime
        total_seconds = int(time_difference.total_seconds())

        if total_seconds < 60:
            i.time_ago = f"{total_seconds} seconds ago"
        elif total_seconds < 3600:
            i.time_ago = f"{total_seconds // 60} minutes ago"
        elif total_seconds < 86400:  # Less than 24 hours
            i.time_ago = f"{total_seconds // 3600} hours ago"
        elif total_seconds < 172800:  # Less than 48 hours (1 day)
            i.time_ago = "1 day ago"
        elif total_seconds < 604800:  # Less than a week
            i.time_ago = f"{total_seconds // 86400} days ago"
        elif total_seconds < 1209600:  # Less than 2 weeks (1 week)
            i.time_ago = "1 week ago"
        else:
            weeks = total_seconds // 604800
            i.time_ago = f"{weeks} weeks ago"

    return render(request, 'user_notification.html', locals())

@login_required
def read_notifications(request, id):
    notification = Notifications.objects.filter(user_id=request.user.id).order_by('-id')
    notification_to_read = Notifications.objects.filter(user_id=request.user.id,id=id)
    count = Cart.objects.filter(user_id=request.user.id).count()

    for i in notification_to_read:
        i.read = True
        i.save()
    notification_count = Notifications.objects.filter(user_id=request.user.id, read=False).count()
    return render(request, 'user_notification.html', locals())
