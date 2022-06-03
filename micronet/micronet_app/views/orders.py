from django.shortcuts import render, redirect
from django.contrib.auth.hashers import check_password
import json

# from ..views.login import CustomerProfile
from ..models.customer import Profile
from django.views import View
from ..models.orders import Order
from ..middlewares.auth import auth_middleware
from django.http import JsonResponse
from datetime import date
from rest_framework.views import APIView
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
import binascii
from django.contrib.auth.models import User
from time import gmtime, strftime


class OrderView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self , request,username ):
        orders_count = Order.objects.count()
        user = User.objects.get(username=username)
        Orders = list(Order.objects.filter(customer_id=user.id))
        print(Orders)
        order_data =[]
        today = strftime("%Y-%m-%d %H:%M:%S", gmtime())
        for item in Orders:
            order_data.append({
            'order_id': item.order_id,
            'products': item.products,
            'customer': item.customer_id,
            'kind': item.kind,
                })
            
        data = {
            'Orders_count': (orders_count),
            "message": f" Order for {user} are below",
            'Orders': (order_data),
            'date': today,
            'payment_status': "pending"          
        }

        return JsonResponse(data)
    
    def post(self, request,username):
        user = User.objects.get(username=username)
        data = json.loads(request.body.decode("utf-8"))
        order_id = data.get('order_id')
        kind = data.get ('kind')
        products = data.get ('products')
        
        value = {
            'order_id': order_id,
            'kind': kind,
            'products': products
        }
        
        error_message = None
        order = Order.objects.create(**value,customer_id=user.id)
        

        if not error_message:
            message = {
               "message": f" Order {order.order_id} Created",
               'values': value
                }
            return JsonResponse(message, status=201)

        else:
            message = {
                'error': "Error occurred while placing the order, Please try again",
                'values': value
            }
            return JsonResponse (message)

    def delete(self, request,username):
        user = User.objects.get(username=username)
        Orders = list(Order.objects.filter(customer_id=user.id))
        for order in Orders:
            order.delete()

        data = {
            'message': f'All orders have been deleted'
        }

        return JsonResponse(data, status=202)
   
# @method_decorator(csrf_exempt, name='dispatch')
class orderUpdate(APIView):
    permission_classes = [IsAuthenticated]
    def post(self, request,username, order_id, *args, **kwargs):
        data = json.loads(request.body.decode("utf-8"))
        user = User.objects.get(username=username)
        items = list(Order.objects.filter(customer_id=user.id))
        print(items)
        if(len(items) != 0):
            for item in items:
                item_id = item.order_id
                if(item_id == str(order_id)):
                    item = Order.objects.get(order_id=order_id)
                    if("products" in data):
                        item.products = data["products"]
                    if("radiometricProcessing" in data):
                        item.radiometricProcessing  = data["radiometricProcessing"]
                    if("imageFormat" in data):
                        item.imageFormat = data["imageFormat"]
                    if("aoi" in data):
                        item.aoi = data["aoi"]
                    item.save()
                    return_data = {
                        'message': f'Info of order {order_id} has been updated'
                    }
                    status = 201
                    break
                else:
                    return_data = {
                    'message': f'order {order_id} does not exist'
                    }
                status = 400
        else:
            return_data = {
                'message': f'order {order_id} does not exist'
                }
            status = 400

        return JsonResponse(return_data, status=status)

    def delete(self, request,username,order_id):
        user = User.objects.get(username=username)
        items = list(Order.objects.filter(customer_id=user.id))
        if(len(items) != 0):
            for item in items:
                item_id = item.order_id
                if(item_id == order_id):
                    item = Order.objects.get(order_id=order_id)
                    item.delete()
                    status = 202
                    break
                else:
                    return_data = {
                    'message': f'order {order_id} does not exist'
                    }
                status = 400
        else:
            return_data = {
                'message': f'order {order_id} does not exist'
                }
            status = 400

        return_data = {
            'message': f'order {order_id} has been deleted'
        }

        return JsonResponse(return_data, status=status)
    
    def get(self, request,username, order_id):
        user = User.objects.get(username=username)
        items = list(Order.objects.filter(customer_id=user.id))
        if(len(items) != 0):
            for item in items:
                item_id = item.promotion_id
                if(item_id == order_id):
                    item = Order.objects.get(order_id=order_id)
                    return_data = {
                        'order_id': order_id,
                        'kind': item.kind,
                        'products': item.products
                    }
                    status = 200
                    break
                else:
                    return_data = {
                    'message': f'Order {order_id} does not exist'
                    }
                    status = 400
        else:
            return_data = {
                'message': f'Order {order_id} does not exist'
                }
            status = 400

        return JsonResponse(return_data, status = status)
    
    

