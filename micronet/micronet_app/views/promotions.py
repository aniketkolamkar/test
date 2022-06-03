import json
import requests
from django.http import JsonResponse
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
from datetime import date
from rest_framework.views import APIView
from ..views.providers import Provider
from rest_framework.permissions import IsAuthenticated
from ..models.promotions import Promotions

class PromotionsView(APIView):
    permission_classes = [IsAuthenticated]
    def post(self, request):
        data = json.loads(request.body.decode("utf-8"))
        
        promotion_id = data.get('promotion_id')
        provider = data.get('provider')
        promotype = data.get('promotype')
        start_date = data.get('start_date')
        end_date = data.get('end_date')

        data = {
            "promotion_id" : promotion_id,
            "provider" : provider,
            "promotype" : promotype,
            "start_date" : start_date,
            "end_date" : end_date
        }

        promotion = Promotions.objects.create(**data)

        data = {
            "message": f"New Promotions {promotion.promotion_id} added Successfully"
        }
        return JsonResponse(data, status=201)
    
    def get(self, request):
        items_count = Promotions.objects.count()
        items = Promotions.objects.all()

        items_data = []
        for item in items:
            items_data.append({
                "promotion_id" : item.promotion_id,
                "provider" : item.provider,
                "promotype" : item.promotype,
                "start_date" : item.start_date,
                "end_date" : item.end_date
            })

        data = {
            'Promotions': items_data,
            'Promotions_count': items_count,
        }

        return JsonResponse(data)
    
    def delete(self, request):
        items = Promotions.objects.all()
        for item in items:
            item.delete()

        data = {
            'message': f'All Promotions have been deleted'
        }

        return JsonResponse(data, status=202)

@method_decorator(csrf_exempt, name='dispatch')
class promotionUpdate(APIView):

    def post(self, request, promotion_id):
        data = json.loads(request.body.decode("utf-8"))
        items = Promotions.objects.all()
        if(len(items) != 0):
            for item in items:
                item_id = item.promotion_id
                if(item_id == promotion_id):
                    item = Promotions.objects.get(promotion_id=promotion_id)
                    if("promotype" in data):
                        item.promotype = data["promotype"]
                    if("provider" in data):
                        item.provider  = data["provider"]
                    if("start_date" in data):
                        item.start_date = data["start_date"]
                    if("end_date" in data):
                        item.end_date = data["end_date"]
                    item.save()
                    return_data = {
                        'message': f'Info of promotion {promotion_id} has been updated'
                    }
                    status = 201
                    break
                else:
                    return_data = {
                    'message': f'promotion {promotion_id} does not exist'
                    }
                status = 400
        else:
            return_data = {
                'message': f'promotion {promotion_id} does not exist'
                }
            status = 400

        return JsonResponse(return_data, status=status)

    def delete(self, request,promotion_id):
        items = list(Promotions.objects.all())
        if(len(items) != 0):
            for item in items:
                item_id = item.promotion_id
                if(item_id == promotion_id):
                    item = Promotions.objects.get(promotion_id=promotion_id)
                    item.delete()
                    status = 202
                    break
                else:
                    return_data = {
                    'message': f'promotion {promotion_id} does not exist'
                    }
                status = 400
        else:
            return_data = {
                'message': f'promotion {promotion_id} does not exist'
                }
            status = 400

        return_data = {
            'message': f'promotion {promotion_id} has been deleted'
        }

        return JsonResponse(return_data, status=status)
    
    def get(self, request, promotion_id):
        items = list(Promotions.objects.all())
        if(len(items) != 0):
            for item in items:
                item_id = item.promotion_id
                if(item_id == promotion_id):
                    item = Promotions.objects.get(promotion_id=promotion_id)
                    return_data = {
                        "promotion_id" : item.promotion_id,
                        "provider" : item.provider,
                        "promotype" : item.promotype,
                        "start_date" : item.start_date,
                        "end_date" : item.end_date
                    }
                    status = 200
                    break
                else:
                    return_data = {
                    'message': f'promotion {promotion_id} does not exist'
                    }
                    status = 400
        else:
            return_data = {
                'message': f'promotion {promotion_id} does not exist'
                }
            status = 400

        return JsonResponse(return_data, status = status)
    
    
