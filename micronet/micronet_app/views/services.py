import json
import requests
from django.http import JsonResponse
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
from datetime import date
from rest_framework.views import APIView
from ..views.providers import Provider
from rest_framework.permissions import IsAuthenticated
from ..models.services import Services

class ServicesView(APIView):
    permission_classes = [IsAuthenticated]
    def post(self, request):
        data = json.loads(request.body.decode("utf-8"))
        
        service_id = data.get('service_id')
        name = data.get('name')
        type = data.get('type')
        cost = data.get('cost')
        currencyunit = data.get('currencyunit')

        data = {
            "service_id" : service_id,
            "name" : name,
            "type" : type,
            "cost" : cost,
            "currencyunit" : currencyunit
        }

        service = Services.objects.create(**data)

        data = {
            "message": f"New Services {service.service_id} added Successfully"
        }
        return JsonResponse(data, status=201)
    
    def get(self, request):
        items_count = Services.objects.count()
        items = Services.objects.all()

        items_data = []
        for item in items:
            items_data.append({
                "service_id" : item.service_id,
                "name" : item.name,
                "type" : item.type,
                "provider" : item.provider,
                "cost" : item.cost,
                "currencyunit" : item.currencyunit
            })

        data = {
            'Services': items_data,
            'Services_count': items_count,
        }

        return JsonResponse(data)
    
    def delete(self, request):
        items = Services.objects.all()
        for item in items:
            item.delete()

        data = {
            'message': f'All Services have been deleted'
        }

        return JsonResponse(data, status=202)

@method_decorator(csrf_exempt, name='dispatch')
class serviceUpdate(APIView):

    def post(self, request, service_id):
        data = json.loads(request.body.decode("utf-8"))
        items = Services.objects.all()
        if(len(items) != 0):
            for item in items:
                item_id = item.service_id
                if(item_id == service_id):
                    item = Services.objects.get(service_id=service_id)
                    if("name" in data):
                        item.name = data["name"]
                    if("type" in data):
                        item.type = data["type"]
                    if("provider" in data):
                        item.provider  = data["provider"]
                    if("cost" in data):
                        item.cost = data["cost"]
                    if("currencyunit" in data):
                        item.currencyunit = data["currencyunit"]
                    item.save()
                    return_data = {
                        'message': f'Info of service {service_id} has been updated'
                    }
                    status = 201
                    break
                else:
                    return_data = {
                    'message': f'service {service_id} does not exist'
                    }
                status = 400
        else:
            return_data = {
                'message': f'service {service_id} does not exist'
                }
            status = 400

        return JsonResponse(return_data, status=status)

    def delete(self, request,service_id):
        items = list(Services.objects.all())
        if(len(items) != 0):
            for item in items:
                item_id = item.service_id
                if(item_id == service_id):
                    item = Services.objects.get(service_id=service_id)
                    item.delete()
                    status = 202
                    break
                else:
                    return_data = {
                    'message': f'service {service_id} does not exist'
                    }
                status = 400
        else:
            return_data = {
                'message': f'service {service_id} does not exist'
                }
            status = 400

        return_data = {
            'message': f'service {service_id} has been deleted'
        }

        return JsonResponse(return_data, status=status)
    
    def get(self, request, service_id):
        items = list(Services.objects.all())
        if(len(items) != 0):
            for item in items:
                item_id = item.service_id
                if(item_id == service_id):
                    item = Services.objects.get(service_id=service_id)
                    return_data = {
                        "service_id" : item.service_id,
                        "name" : item.name,
                        "type" : item.type,
                        "provider" : item.provider,
                        "cost" : item.cost,
                        "currencyunit" : item.currencyunit
                    }
                    status = 200
                    break
                else:
                    return_data = {
                    'message': f'service {service_id} does not exist'
                    }
                    status = 400
        else:
            return_data = {
                'message': f'service {service_id} does not exist'
                }
            status = 400

        return JsonResponse(return_data, status = status)
    
    
