# from django.shortcuts import render, redirect
# from django.contrib.auth.hashers import make_password
# from ..models.customer import  Profile
# import json
# from django.views import View
# from django.http import JsonResponse
# from django.utils.decorators import method_decorator
# from django.views.decorators.csrf import csrf_exempt
# from django.shortcuts import render , redirect , HttpResponseRedirect
# from django.contrib.auth.hashers import  check_password
# from rest_framework.views import APIView
# from rest_framework.decorators import api_view, permission_classes
# from rest_framework.permissions import IsAuthenticated

# @method_decorator(csrf_exempt, name='dispatch')
# class CustomerView(APIView):
#     permission_classes = [IsAuthenticated]
#     def get(self, request,customer_id):
#         customer = Customer.objects.get(id=customer_id)
#         #Orders = CartItem.objects.all()
#         order_data =[]
#         customers_data = []
#         # for customer in customers:
        
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
#             'email': customer.email
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

# from rest_framework import status
# from rest_framework import generics
# from rest_framework.response import Response
# from django.contrib.auth.models import User
# from ..serializers import ChangePasswordSerializer
# from rest_framework.permissions import IsAuthenticated 

# class ChangePasswordView(generics.UpdateAPIView):
#         """
#         An endpoint for changing password.
#         """
#         serializer_class = ChangePasswordSerializer
#         model = User
#         permission_classes = (IsAuthenticated,)

#         def get_object(self, queryset=None):
#             obj = self.request.user
#             return obj

#         def update(self, request, *args, **kwargs):
#             self.object = self.get_object()
#             serializer = self.get_serializer(data=request.data)

#             if serializer.is_valid():
#                 # Check old password
#                 if not self.object.check_password(serializer.data.get("old_password")):
#                     return Response({"old_password": ["Wrong password."]}, status=status.HTTP_400_BAD_REQUEST)
#                 # set_password also hashes the password that the user will get
#                 self.object.set_password(serializer.data.get("new_password"))
#                 self.object.save()
#                 response = {
#                     'status': 'success',
#                     'code': status.HTTP_200_OK,
#                     'message': 'Password updated successfully',
#                     'data': []
#                 }

#                 return Response(response)

#             return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)