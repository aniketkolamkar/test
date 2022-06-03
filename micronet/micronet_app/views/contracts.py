import json
import requests
from django.http import JsonResponse
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
from datetime import date
from rest_framework.views import APIView
from ..views.providers import Provider
from rest_framework.permissions import IsAuthenticated
from ..models.contracts import Contracts

class ContractsView(APIView):
    permission_classes = [IsAuthenticated]
    def post(self, request, provider_name):
        provider = Provider.objects.get(provider_name=provider_name)
        data = json.loads(request.body.decode("utf-8"))
        
        contract_id = data.get('contract_id')
        name = data.get('name')
        status = data.get('status')
        createdAt = data.get('createdAt')
        balanceUnit = data.get('balanceUnit')
        balance = data.get('balance')
        kind = data.get('kind')
        workspaceId = data.get('workspaceId')

        data = {
            "contract_id" : contract_id,
            "name" : name,
            "status" : status,
            "createdAt" : createdAt,
            "balanceUnit" : balanceUnit,
            "balance" : balance,
            "kind" : kind,
            "workspaceId" : workspaceId
        }

        contract = Contracts.objects.create(**data,provider=provider)

        data = {
            "message": f"New Contract {contract.contract_id} added for Provider : {provider.provider_name}"
        }
        return JsonResponse(data, status=201)
    
    def get(self, request, provider_name):
        items_count = Contracts.objects.count()
        provider = Provider.objects.get(provider_name=provider_name)
        items = list(Contracts.objects.filter(provider=provider.id))
        print(items)

        items_data = []
        for item in items:
            items_data.append({
                "contract_id" : item.contract_id,
                "name" : item.name,
                "status" : item.status,
                "createdAt" : item.createdAt,
                "balanceUnit" : item.balanceUnit,
                "balance" : item.balance,
                "kind" : item.kind,
                "workspaceId" : item.workspaceId
            })

        data = {
            'contracts': items_data,
            'contracts_count': items_count,
        }

        return JsonResponse(data)
    
    def delete(self, request, provider_name):
        provider = Provider.objects.get(provider_name=provider_name)
        items = list(Contracts.objects.filter(provider=provider.id))
        for item in items:
            item.delete()

        data = {
            'message': f'All Contracts for provider {provider_name} have been deleted'
        }

        return JsonResponse(data, status=202)

@method_decorator(csrf_exempt, name='dispatch')
class ContractUpdate(APIView):

    def post(self, request, provider_name, contract_id):
        data = json.loads(request.body.decode("utf-8"))
        provider = Provider.objects.get(provider_name=provider_name)
        items = list(Contracts.objects.filter(provider=provider.id))
        if(len(items) != 0):
            for item in items:
                item_id = item.contract_id
                if(item_id == contract_id):
                    item = Contracts.objects.get(contract_id=contract_id)
                    if("name" in data):
                        item.name = data["name"]
                    if("status" in data):
                        item.status = data["status"]
                    if("createdAt" in data):
                        item.createdAt  = data["createdAt"]
                    if("balanceUnit" in data):
                        item.balanceUnit = data["balanceUnit"]
                    if("balance" in data):
                        item.balance = data["balance"]
                    if("kind" in data):
                        item.kind = data["kind"]
                    item.save()
                    return_data = {
                        'message': f'Info of Contract {contract_id} for Provider {provider_name} has been updated'
                    }
                    status = 201
                    break
                else:
                    return_data = {
                    'message': f'Contract {contract_id} does not exist'
                    }
                status = 400
        else:
            return_data = {
                'message': f'Contract {contract_id} does not exist'
                }
            status = 400

        return JsonResponse(return_data, status=status)

    def delete(self, request, provider_name, contract_id):
        provider = Provider.objects.get(provider_name=provider_name)
        items = list(Contracts.objects.filter(provider=provider.id))
        if(len(items) != 0):
            for item in items:
                item_id = item.contract_id
                if(item_id == contract_id):
                    item = Contracts.objects.get(contract_id=contract_id)
                    item.delete()
                    status = 202
                    break
                else:
                    return_data = {
                    'message': f'Contract {contract_id} does not exist'
                    }
                status = 400
        else:
            return_data = {
                'message': f'Contract {contract_id} does not exist'
                }
            status = 400

        return_data = {
            'message': f'Contract {contract_id} has been deleted'
        }

        return JsonResponse(return_data, status=status)
    
    def get(self, request, provider_name, contract_id):
        provider = Provider.objects.get(provider_name=provider_name)
        items = list(Contracts.objects.filter(provider=provider.id))
        if(len(items) != 0):
            for item in items:
                item_id = item.contract_id
                if(item_id == contract_id):
                    item = Contracts.objects.get(contract_id=contract_id)
                    return_data = {
                        "contract_id" : item.contract_id,
                        "name" : item.name,
                        "status" : item.status,
                        "createdAt" : item.createdAt,
                        "balanceUnit" : item.balanceUnit,
                        "balance" : item.balance,
                        "kind" : item.kind,
                        "workspaceId" : item.workspaceId
                    }
                    status = 200
                    break
                else:
                    return_data = {
                    'message': f'Contract {contract_id} does not exist'
                    }
                    status = 400
        else:
            return_data = {
                'message': f'Contract {contract_id} does not exist'
                }
            status = 400

        return JsonResponse(return_data, status = status)
    
    
