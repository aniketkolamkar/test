# from django.shortcuts import render, redirect
# from django.contrib.auth.hashers import make_password
# from models.customer import Profile
# import json
# from django.views import View
# from django.http import JsonResponse
# # from ..models.cart import CartItem
# from django.utils.decorators import method_decorator
# from django.views.decorators.csrf import csrf_exempt
# from django.shortcuts import render , redirect , HttpResponseRedirect
# from django.contrib.auth.hashers import  check_password
# from rest_framework.views import APIView
# from rest_framework.decorators import api_view, permission_classes
# from rest_framework.permissions import IsAuthenticated

# from rest_framework.response import Response
# from rest_framework.decorators import api_view, permission_classes
# from rest_framework.permissions import IsAuthenticated, AllowAny

# from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
# from rest_framework_simplejwt.views import TokenObtainPairView
# from rest_framework_simplejwt.authentication import JWTTokenUserAuthentication

# from django.contrib.auth.models import User


# @method_decorator(csrf_exempt, name='dispatch')
# class CustomerView(APIView):
#     permission_classes = [IsAuthenticated]
#     def get(self, request,customer_id):
#         # customer = Customer.objects.get(id=customer_id)
#         # Orders = CartItem.objects.all()
#         # order_data =[]
#         # # customers_data = []
#         # # for customer in customers:
        
#         # for order in Orders:
#         #     order_data.append({
#         #         'product': order.product_name,
#         #         'customer': customer_id,
#         #         'quantity': order.product_quantity,
#         #         'price': order.product_price
#         #           })
    
#         customers_data = {
#             'customer':{ # 'customer_detail': customers_data,
#             'customer_id': customer.id,
#             'first_name': customer.first_name,
#             'last_name': customer.last_name,
#             'phone': customer.phone,
#             'email': customer.email,
#             # 'cart_details': (order_data)
#             # 'cart_details': (order_data)
#           }
           
            
#         }

#         return JsonResponse(customers_data)
# @method_decorator(csrf_exempt, name='dispatch')
# class Login(View):
#     return_url = None

#     def post(self, request):
#         data = json.loads(request.body.decode("utf-8"))
#         email = data.get ('email')
#         password = data.get ('password')
#         customer = Customer.get_customer_by_email (email)
#         #print (customer)
#         error_message = None
#         if customer:
#             # print(customer.password)
#             # flag = check_password (password, customer.password)
#             if (password == customer.password):
#                 request.session['customer'] = customer.id

#                 if Login.return_url:
#                     return HttpResponseRedirect (Login.return_url)
#                 else:
#                     Login.return_url = None
#                     message = {
#                     "message": "Login Successful"
#                     }
#                     return JsonResponse (message, status=201)
#             else:
#                 error_message = 'Invalid !!'
#         else:
#             error_message = 'Invalid !!'

#         print (email, password)
#         message = {
#                 "message": error_message
#                 }
#         return JsonResponse (message, status=201)

# def logout(request):
#     request.session.clear()
#     return redirect('login')

# @method_decorator(csrf_exempt, name='dispatch')
# class CustomerUpdate(View):

#     def patch(self, request, customer_id):
#         data = json.loads(request.body.decode("utf-8"))
#         customer = Customer.objects.get(id=customer_id)
#         customer.first_name = data['first_name']
#         customer.last_name = data['last_name']
#         customer.phone = data['phone']

#         customer.save()

#         message = {
#             'message': f'Item {customer_id} has been updated'
#         }

#         return JsonResponse(message, status=201)

#     def delete(self, request, customer_id):
#         customer = Customer.objects.get(id=customer_id)
#         customer.delete()
#         customerrofile = Profile.objects.get(customer_id=customer_id)
#         customerrofile.delete()

#         message = {
#             'message': f'Item {customer_id} has been deleted'
#         }

#         return JsonResponse(message, status=202)

# @method_decorator(csrf_exempt, name='dispatch')
# class CustomerProfileUpdate(View):

#     def post(self, request, customer_id):
#         data = json.loads(request.body.decode("utf-8"))
#         customerProfile = Profile.objects.get(customer_id=customer_id)
#         customerProfile.customer_id = data['customer_id']
#         if "address" in data:
#             customerProfile.address = data['address']
#         # if "past_orders" in data:
#         #     customerProfile.past_orders = data['past_orders']
#         # if "wishlist" in data:
#         #     customerProfile.wishlist = data['wishlist']

#         #print(json.dumps(customerProfile))

        
#         customerProfile.save()

#         message = {
#             'message': f'Profile for customer ID {customer_id} has been updated'
#         }

#         return JsonResponse(message, status=201)


# @method_decorator(csrf_exempt, name='dispatch')
# class CustomerProfile(View):

#     def get(self, request, customer_id):
#         customerProfile = Profile.objects.all()

#         customerProfile = Profile.objects.get(customer_id=customer_id)

#         customerProfile = {
#             'customer_id': customerProfile.customer_id,
#             'address': customerProfile.address,
#             # 'past_orders': customerProfile.past_orders,
#             # 'wishlist': customerProfile.wishlist
#         }

#         return JsonResponse(customerProfile)


# @method_decorator(csrf_exempt, name='dispatch')
# class Signup(APIView):
#     permission_classes = [IsAuthenticated]
#     def get(self, request):
#         customers_count = Customer.objects.count()
#         customers = Customer.objects.all()
#         #permission_classes = (IsAuthenticated,)

#         customers_data = []
#         for customer in customers:
#             customers_data.append({
#                 'customer_id': customer.id,
#                 'first_name': customer.first_name,
#                 'last_name': customer.last_name,
#                 'phone': customer.phone,
#                 'email': customer.email,
#                 'password': customer.password
#             })

#         data = {
#             'customers': customers_data,
#             'count': customers_count,
#         }

#         return JsonResponse(data)

#     # @permission_classes([IsAuthenticated])
#     def post(self, request):
#         data = json.loads(request.body.decode("utf-8"))
#         # postData = request.POST
#         first_name = data.get ('first_name')
#         last_name = data.get ('last_name')
#         phone = data.get ('phone')
#         email = data.get ('email')
#         password = data.get ('password')
#         # permission_classes = (IsAuthenticated,)
#         # validation
#         value = {
#             'first_name': first_name,
#             'last_name': last_name,
#             'phone': phone,
#             'email': email,
#             'password': password
#         }
        
#         error_message = None

        
#         error_message = self.validateCustomer (value)
#         if Customer.objects.filter(email = value.get("email")):
#             data = {
#                 "message": f"User Already Exists"
#                 }
#             return JsonResponse(data, status=403)

#         if not error_message:
#             customer = Customer.objects.create(**value)
#             customerid = Customer.get_customer_by_email (email)

#             profile = {
#             'customer_id': customerid.id,
#             'address': ""
#             }
#             customerprofile = Profile.objects.create(**profile)
#             print (first_name, last_name, phone, email, password)
#             customer.password = make_password (customer.password)
#             customer.register ()
#             message = {
#                 "message": f"New User created :{customer}"
#                 }
#             return JsonResponse(message, status=201)

#         else:
#             message = {
#                 'error': error_message,
#                 'values': value
#             }
#             return JsonResponse (message)

#     # @permission_classes([IsAuthenticated])
#     def validateCustomer(self, customer):
#         # permission_classes = (IsAuthenticated,)
#         error_message = None
#         if ("first_name" not in customer):
#             error_message = "Please Enter your First Name !!"
#         elif len (customer.get("first_name")) < 3:
#             error_message = 'First Name must be 3 char long or more'
#         elif ("last_name" not in customer):
#             error_message = 'Please Enter your Last Name'
#         elif len (customer.get("last_name")) < 3:
#             error_message = 'Last Name must be 3 char long or more'
#         elif ("phone" not in customer):
#             error_message = 'Enter your Phone Number'
#         elif len (customer.get("phone")) < 10:
#             error_message = 'Phone Number must be 10 char Long'
#         elif ("password" not in customer):
#             error_message = 'Enter your Password' 
#         elif len (customer.get("password")) < 5:
#             error_message = 'Password must be 5 char long'
#         elif ("email" not in customer):
#             error_message = 'Enter your Email'
#         elif len (customer.get("email")) < 5:
#             error_message = 'Email must be 5 char long'
#         # elif customer.isExists ():
#         #     error_message = 'Email Address Already Registered..'
#         # saving

#         return error_message


# class MyTokenObtainPairSerializer(TokenObtainPairSerializer):
#     @classmethod
#     def get_token(cls, user):
#         token = super().get_token(user)

#         # Add custom claims
#         token['username'] = user.username
#         # ...

#         return token


# class MyTokenObtainPairView(TokenObtainPairView):
#     serializer_class = MyTokenObtainPairSerializer

# permission_classes = (IsAuthenticated)
# authentication_class = JWTTokenUserAuthentication

# @api_view(['GET'])
# def getRoutes(request):
#     routes = [
#         '/api/token',
#         '/api/token/refresh',
#     ]

#     return Response(routes)
