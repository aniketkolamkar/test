from django.views import View
from django.http import JsonResponse
import json
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from sqlalchemy import null
from ..models.providers import Provider


@method_decorator(csrf_exempt, name='dispatch')
class Providers(APIView):
    permission_classes = [IsAuthenticated]
    def post(self, request):

        data = json.loads(request.body.decode("utf-8"))
        provider_name = data.get('provider_name')
        label = data.get('label')
        status = data.get('status')
        api_key = data.get('api_key')
        links = data.get('links')

        data = {
            "provider_name" : provider_name,
            "label" : label,
            "status" : status,
            "api_key" : api_key,
            "links" : links
        }

        provider = Provider.objects.create(**data)

        data = {
            "message": f"New provider added br name: {provider.provider_name}"
        }
        return JsonResponse(data, status=201)
    
    def get(self, request):
        items_count = Provider.objects.count()
        items = Provider.objects.all()

        items_data = []
        for item in items:
            items_data.append({
                "provider_name" : item.provider_name,
                "label" : item.label,
                "status" : item.status,
                "api_key" : item.api_key,
                "links" : item.links
            })

        data = {
            'items': items_data,
            'count': items_count,
        }

        return JsonResponse(data)
    
    def delete(self, request):
        items = Provider.objects.all()
        for item in items:
            item.delete()

        data = {
            'message': f'All providers have been deleted'
        }

        return JsonResponse(data)

@method_decorator(csrf_exempt, name='dispatch')
class ProviderUpdate(APIView):

    def post(self, request, provider_name):
        data = json.loads(request.body.decode("utf-8"))
        items = Provider.objects.all()
        if(len(items) != 0):
            for item in items:
                name = item.provider_name
                if(name == provider_name):
                    provider = Provider.objects.get(provider_name=provider_name)
                    if("label" in data):
                        provider.label = data['label']
                    if("status" in data):
                        provider.status = data['status']
                    if("api_key" in data):
                        provider.api_key = data['api_key']
                    if("links" in data):
                        provider.links = data['links']
                    provider.save()
                    return_data = {
                        'message': f'Provider {provider_name} info has been updated'
                        }
                    status = 201
                    break
                else:
                    return_data = {
                    'message': f'Provider {provider_name} does not exist'
                    }
                    status = 400
        else:
            return_data = {
                'message': f'Provider {provider_name} does not exist'
                }
            status = 400
        return JsonResponse(return_data,status=status)

    def delete(self, request, provider_name):
        items = Provider.objects.all()
        if(len(items) != 0):
            for item in items:
                name = item.provider_name
                if(name == provider_name):
                    provider = Provider.objects.get(provider_name=provider_name)
                    item.delete()
                    data = {
                        'message': f'Item {provider_name} has been deleted'
                    }
                    status = 202
                    
                else:
                    return_data = {
                    'message': f'Provider {provider_name} does not exist'
                    }
                status = 400
        else:
            return_data = {
                'message': f'Provider {provider_name} does not exist'
                }
            status = 400

        return JsonResponse(data, status=status)
    
    def get(self, request,provider_name):
        items = Provider.objects.all()
        if(len(items) != 0):
            for item in items:
                name = item.provider_name
                if(name == provider_name):
                    provider = Provider.objects.get(provider_name=provider_name)
                    data = {
                        "provider_name" : item.provider_name,
                        "label" : item.label,
                        "status" : item.status,
                        "api_key" : item.api_key,
                        "links" : item.links
                    }
                    status = 200
                    break
                else:
                    return_data = {
                    'message': f'Provider {provider_name} does not exist'
                    }
                    status = 400
        else:
            return_data = {
                'message': f'Provider {provider_name} does not exist'
                }
            status = 400

        return JsonResponse(data, status=status)
    