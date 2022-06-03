from django.contrib import admin

from .models.orders import Order
from .models.customer import Profile
# from .models.payment import Payment
# from .models.promotion import Promotion


# admin.site.register(Customer/)
admin.site.register(Profile)
admin.site.register(Order)
# from django.contrib.auth.admin import GroupAdmin
# from django.contrib.auth.models import Group

# from .models import Role


# admin.site.unregister(Group)
# admin.site.register(Role, GroupAdmin)
#admin.site.register(Category)
# admin.site.register(Payment)
# admin.site.register(Promotion)



# from django.contrib import admin
# from django.contrib.auth.admin import UserAdmin

# # from .forms import UserCreationForm, UserChangeForm
# # from .models import User
# from micronet_app.serializers import RegisterSerializer
