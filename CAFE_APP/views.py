from django.http import Http404, HttpResponse
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.conf import settings
from datetime import datetime, timedelta
from django.contrib import messages
import re
from django.utils import timezone
from .models import *
from .models import Notifications, Cart, Food_items, Orders, Address, Blog, Contact
# from django.contrib.auth.models import User
from django.contrib.auth import get_user_model
from datetime import date


# Create your views here.

def index(request):
    data = Food_items.objects.all()
    blogs = Blog.objects.all()
    return render(request, 'index.html', locals())


@login_required
def user_home(request):
    notification_count = Notifications.objects.filter(
        user_id=request.user.id, read=False
    ).count()

    count = Cart.objects.filter(user_id=request.user.id).count()

    data = Food_items.objects.all()

    # Safe profile_id extraction
    profile_id = getattr(getattr(request.user, "profile", None), "id", None)

    context = {
        'user': request.user,
        'profile_id': profile_id,
        'notification_count': notification_count,
        'count': count,
        'data': data,
    }
    return render(request, 'user_home.html', context)

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
    new_orders = Orders.objects.filter(status=1).order_by('-order_time')
    accepted_orders = Orders.objects.filter(status=2).order_by('-order_time')
    delivered_orders = Orders.objects.filter(status=3).order_by('-order_time')
    cancelled_orders = Orders.objects.filter(status=4).order_by('-order_time')

    # Attach coffee item to each order
    for order in list(new_orders) + list(accepted_orders) + list(delivered_orders) + list(cancelled_orders):
        order.coffee = Food_items.objects.filter(id=order.item_id).first()

    return render(request, 'admin_orders.html', {
        'new_orders': new_orders,
        'accepted_orders': accepted_orders,
        'delivered_orders': delivered_orders,
        'cancelled_orders': cancelled_orders,
    })




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

    cart_item = Cart.objects.filter(item_id=id, user_id=request.user.id).first()

    if cart_item:
        # If already in cart → increment quantity
        food = get_object_or_404(Food_items, id=id)
        cart_item.quantity += 1
        cart_item.item_total = cart_item.quantity * food.price
        cart_item.save()
    else:
        # If not in cart → create new
        food = get_object_or_404(Food_items, id=id)
        Cart.objects.create(
            item=food,
            user=request.user,
            quantity=1,
            item_total=food.price
        )

    return redirect('coffees')


@login_required
def increment_quantity(request, item_id):
    if request.method == "POST":
        cart_item = get_object_or_404(Cart, id=item_id, user=request.user)
        cart_item.quantity += 1
        cart_item.save()

        # Recalculate grand total
        cart_data = Cart.objects.filter(user=request.user)
        grand_total = sum(item.item_total for item in cart_data)

        return JsonResponse({
            'quantity': cart_item.quantity,
            'item_total': float(cart_item.item_total),
            'grand_total': float(grand_total),
        })


@login_required
def decrement_quantity(request, item_id):
    if request.method == "POST":
        cart_item = get_object_or_404(Cart, id=item_id, user=request.user)
        if cart_item.quantity > 1:
            cart_item.quantity -= 1
            cart_item.save()
        else:
            # If 0 → delete item
            cart_item.delete()

        # Recalculate grand total
        cart_data = Cart.objects.filter(user=request.user)
        grand_total = sum(item.item_total for item in cart_data)

        return JsonResponse({
            'quantity': cart_item.quantity if cart_item.id else 0,
            'item_total': float(cart_item.item_total) if cart_item.id else 0,
            'grand_total': float(grand_total),
            'removed': not cart_item.id,  # Flag for JS
        })


@login_required
def cart_item(request):
    notification_count = Notifications.objects.filter(user_id=request.user.id, read=False).count()
    cart_data = Cart.objects.filter(user_id=request.user.id)
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
    Cart.objects.filter(user_id=request.user.id).delete()
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

@login_required
def profile(request):
    notification_count = Notifications.objects.filter(user_id=request.user.id, read=False).count()
    count = Cart.objects.filter(user=request.user).count()
    profile_user = request.user
    address = Address.objects.filter(user_id=request.user.id)
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
    return redirect('profile')


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
