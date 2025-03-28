from django.contrib import admin
from .models import *
# Register your models here.

admin.site.register(User)
admin.site.register(Food_items)
admin.site.register(Orders)
admin.site.register(Cart)
admin.site.register(Address)
admin.site.register(Blog)
admin.site.register(Contact)
admin.site.register(Notifications)

