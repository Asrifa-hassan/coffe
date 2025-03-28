from django.db import models
from django.contrib.auth.models import AbstractUser
from django.db.models import CharField
# Create your models here.


userchoices = (
    (1, "Admin"),
    (2, "Employee"),
    (3, "Client"),
)

orderstatus = (
    (1, "Ordered"),
    (2, "Pending"),
    (3, "Delivered"),
    (4, "Cancelled")
)

class User(AbstractUser):
    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = ['username', 'phone_number']

    name = models.CharField(max_length=255, null=True, blank=True)
    user_type = models.IntegerField(default=1, choices=userchoices)
    phone_number = models.CharField(max_length=13, null=True, blank=True)
    email = models.EmailField(null=True, blank=True, unique=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        if self.name:
            return self.name
        else:
            return self.username



class Food_items(models.Model):
    item_name = models.CharField(max_length=50, null=True, blank=True)
    item_id = models.CharField(max_length=50, null=True, blank=True)
    description = models.CharField(max_length=225, null=True, blank=True)
    image = models.ImageField(null=True, blank=True, upload_to='images/')
    price = models.DecimalField(decimal_places=2, max_digits=7, null=True, blank=True)

    def __int__(self):
        return self.item_id



class Cart(models.Model):
    item = models.ForeignKey(Food_items,null=True, blank=True, on_delete=models.CASCADE)
    user_id = models.ForeignKey(User, null=True, blank=True, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)
    item_total = models.DecimalField(max_digits=10, decimal_places=2)

    def save(self, *args, **kwargs):
        self.item_total = self.item.price * self.quantity
        super().save(*args, **kwargs)

class Blog(models.Model):
    title = models.CharField(max_length=100, null=True, blank=True)
    image = models.ImageField(null=True, blank=True, upload_to='images/')
    date = models.DateField(auto_now_add=True)
    description = models.TextField(null=True, blank=True)


class Address(models.Model):
    user_id = models.ForeignKey(User, null=True, blank=True, on_delete=models.CASCADE)
    address = models.CharField(max_length=200, null=True, blank=True)
    city = models.CharField(max_length=50, null=True, blank=True)
    phone_number = models.CharField(max_length=13, null=True, blank=True)
    Zipcode = models.CharField(max_length=20, null=True, blank=True)
    Land_Mark = models.CharField(max_length=50, null=True, blank=True)


class Contact(models.Model):
    name = models.CharField(max_length=30, null=True, blank=True)
    email = models.EmailField(null=True, blank=True)
    phone_number = models.CharField(max_length=13, null=True, blank=True)
    message = models.TextField(null=True, blank=True)
    datetime = models.DateTimeField(auto_now_add=True, null=True)

    def __str__(self):
        return self.name

class Orders(models.Model):
    order_id = models.IntegerField(null=True, blank=True,unique=True)
    user_id = models.ForeignKey(User, null=True, blank=True, on_delete=models.CASCADE)
    item = models.ForeignKey(Food_items, null=True, blank=True, on_delete=models.CASCADE)
    quantity = models.IntegerField(null=True, blank=True)
    address = models.ForeignKey(Address, max_length=200, null=True, on_delete=models.CASCADE )
    order_time = models.DateTimeField(auto_now_add=True)
    total_price = models.DecimalField(decimal_places=2, max_digits=7, null=True, blank=True)
    status = models.IntegerField(default=1, choices=orderstatus)


class Notifications(models.Model):
    user_id = models.ForeignKey(User, on_delete=models.CASCADE)
    message = models.TextField()
    read = models.BooleanField(default=False)
    datetime = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.message

