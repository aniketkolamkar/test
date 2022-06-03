from django.views import View
from django.http import JsonResponse
import json
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from ..models.subscriptions import Subscriptions
from ..views.providers import Provider


@method_decorator(csrf_exempt, name='dispatch')
class Subscription(APIView):
    permission_classes = [IsAuthenticated]
    def post(self, request, provider_name):
        provider = Provider.objects.get(provider_name=provider_name)
        data = json.loads(request.body.decode("utf-8"))
        # print("Provider Name = ",provider.provider_name)
        # provider_name = provider.provider_name
        subscription_id = data.get('subscription_id')
        serviceinfo = data.get('serviceinfo')
        status = data.get('status')
        startedAt = data.get('startedAt')
        endedAt = data.get('endedAt')
        type = data.get('type')

        data = {
            "subscription_id" : subscription_id,
            "serviceinfo" : serviceinfo,
            "status" : status,
            "startedAt" : startedAt,
            "endedAt" : endedAt,
            "type" : type
        }
        # s = Subscriptions.objects.prepare_child(provider)

        subscription = Subscriptions.objects.create(**data,provider=provider)

        data = {
            "message": f"New Subscription {subscription.subscription_id} added for Provider : {provider.provider_name}"
        }
        return JsonResponse(data, status=201)
    
    def get(self, request, provider_name):
        items_count = Subscriptions.objects.count()
        provider = Provider.objects.get(provider_name=provider_name)
        items = list(Subscriptions.objects.filter(provider=provider.id))
        print(items)

        items_data = []
        for item in items:
            items_data.append({
                "subscription_id" : item.subscription_id,
                "serviceinfo" : item.serviceinfo,
                "status" : item.status,
                "startedAt" : item.startedAt,
                "endedAt" : item.endedAt,
                "type" : item.type
            })

        data = {
            'subscriptions': items_data,
            'subscription_count': items_count,
        }

        return JsonResponse(data)
    
    def delete(self, request, provider_name):
        provider = Provider.objects.get(provider_name=provider_name)
        items = list(Subscriptions.objects.filter(provider=provider.id))
        for item in items:
            item.delete()

        data = {
            'message': f'All Subscriptions for provider {provider_name} have been deleted'
        }

        return JsonResponse(data, status=202)

@method_decorator(csrf_exempt, name='dispatch')
class SubscriptionUpdate(APIView):

    def post(self, request, provider_name, subscription_id):
        data = json.loads(request.body.decode("utf-8"))
        provider = Provider.objects.get(provider_name=provider_name)
        items = list(Subscriptions.objects.filter(provider=provider.id))
        if(len(items) != 0):
            for item in items:
                item_id = item.subscription_id
                if(item_id == subscription_id):
                    item = Subscriptions.objects.get(subscription_id=subscription_id)
                    if("serviceinfo" in data):
                        item.serviceinfo = data["serviceinfo"]
                    if("status" in data):
                        item.status = data["status"]
                    if("startedAt" in data):
                        item.startedAt = data["startedAt"]
                    if("endedAt" in data):
                        item.endedAt = data["endedAt"]
                    if("type" in data):
                        item.type = data["type"]
                    item.save()
                    return_data = {
                        'message': f'Info of Subscription {subscription_id} for Provider {provider_name} has been updated'
                    }
                    status = 201
                    break
                else:
                    return_data = {
                    'message': f'Subscription {subscription_id} does not exist'
                    }
                status = 400
        else:
            return_data = {
                'message': f'Subscription {subscription_id} does not exist'
                }
            status = 400

        return JsonResponse(return_data, status=status)

    def delete(self, request, provider_name, subscription_id):
        provider = Provider.objects.get(provider_name=provider_name)
        items = list(Subscriptions.objects.filter(provider=provider.id))
        if(len(items) != 0):
            for item in items:
                item_id = item.subscription_id
                if(item_id == subscription_id):
                    item = Subscriptions.objects.get(subscription_id=subscription_id)
                    item.delete()
                    status = 202
                    break
                else:
                    return_data = {
                    'message': f'Subscription {subscription_id} does not exist'
                    }
                status = 400
        else:
            return_data = {
                'message': f'Subscription {subscription_id} does not exist'
                }
            status = 400

        return_data = {
            'message': f'Subscription {subscription_id} does not exist'
        }

        return JsonResponse(return_data, status=status)
    
    def get(self, request, provider_name, subscription_id):
        provider = Provider.objects.get(provider_name=provider_name)
        items = list(Subscriptions.objects.filter(provider=provider.id))
        if(len(items) != 0):
            for item in items:
                item_id = item.subscription_id
                if(item_id == subscription_id):
                    item = Subscriptions.objects.get(subscription_id=subscription_id)
                    return_data = {
                        "subscription_id" : item.subscription_id,
                        "serviceinfo" : item.serviceinfo,
                        "status" : item.status,
                        "startedAt" : item.startedAt,
                        "endedAt" : item.endedAt,
                        "type" : item.type
                    }
                    status = 200
                    break
                else:
                    return_data = {
                    'message': f'Subscription {subscription_id} does not exist'
                    }
                    status = 400
        else:
            return_data = {
                'message': f'Subscription {subscription_id} does not exist'
                }
            status = 400

        return JsonResponse(return_data, status = status)
    