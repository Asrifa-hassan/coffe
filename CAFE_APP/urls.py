from django.urls import path
from . import views


urlpatterns = [
    path('', views.index, name='index'),
    path('about/', views.about, name='about'),
    path('coffees/', views.coffees, name='coffees'),
    path('blog/', views.blog, name='blog'),
    path('contact/', views.contact, name='contact'),
    path('login_page/', views.login_page, name='login_page'),
    path('cofe_read/<int:id>', views.cofe_read, name='cofe_read'),
    path('blog_read/<int:id>', views.blog_read, name='blog_read'),
    path('register/', views.Registration, name='register'),
    path('login_function/', views.login_function, name='login_function'),
    path('forgot_password/', views.forgot_password, name='forgot_password'),
    path('logout/', views.logout_function, name='logout'),


    # ------------ user module--------------------------
    path('user_home/', views.user_home, name='user_home'),
    path('cart-item/', views.cart_item, name='cart_item'),
    path('add_to_cart/<int:id>', views.add_to_cart, name='add_to_cart'),
    path('increment/<int:item_id>/', views.increment_quantity, name='increment_quantity'),
    path('decrement/<int:item_id>/', views.decrement_quantity, name='decrement_quantity'),
    path('delete_cart_item/<int:id>', views.delete_cart_item, name='delete_cart_item'),
    path('order_items/', views.order_items, name='order_items'),
    path('empty_cart/', views.empty_cart, name='empty_cart'),
    path('profile/', views.profile, name='profile'),
    path('add_address/', views.add_address, name='add_address'),
    path('get_address/<int:id>', views.get_address, name='get_address'),
    path('change_address/<int:id>', views.change_address, name='change_address'),
    path('delete_address/<int:id>', views.delete_address, name='delete_address'),
    path('user_notification/', views.user_notification, name='user_notification'),
    path('read_notifications/<int:id>/', views.read_notifications, name='read_notifications'),


    #------------- admin module -----------------------
    path('dashboard/', views.Dashboard, name='dashboard'),
    path('admin_products/', views.admin_products, name='admin_products'),
    path('admin_view_product/<int:id>', views.admin_view_product, name='admin_view_product'),
    path('add_item/', views.add_item, name='add_item'),
    path('edit_item/<int:id>', views.edit_item, name='edit_item'),
    path('delete_item/<int:id>', views.delete_item, name='delete_item'),
    path('Accept_item/<int:id>', views.Accept_item, name='Accept_item'),
    path('Cancel_item/<int:id>', views.Cancel_item, name='Cancel_item'),
    path('Pending_item/<int:id>', views.Pending_item, name='Pending_item'),
    path('admin_orders/', views.admin_orders, name='admin_orders'),
    path('notification_admin/', views.notification_admin, name='notification_admin'),
    path('admin_users/', views.admin_users, name='admin_users'),
    path('admin_contact/', views.admin_contact, name='admin_contact'),
    path('admin_blog/', views.admin_blog, name='admin_blog'),
    path('add_blog/', views.add_blog, name='add_blog'),
    path('edit_blog/<int:id>', views.edit_blog, name='edit_blog'),
    path('delete_blog/<int:id>', views.delete_blog, name='delete_blog'),
    path('admin_view_blog/<int:id>', views.admin_view_blog, name='admin_view_blog'),

]
