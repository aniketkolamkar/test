from django.shortcuts import render, redirect
import json
import requests
import time

from sqlalchemy import null
from ..models.search import Search
from ..models.orders import Order
from ..middlewares.auth import auth_middleware
from django.http import JsonResponse
from datetime import date
from rest_framework.views import APIView
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from django.contrib.auth.models import User
from ..models.subscriptions import Subscriptions
from ..views.providers import Provider

class SavedSearchView(APIView):
    permission_classes = [IsAuthenticated]
    
    def post(self, request, username):
        users = User.objects.all()
        if(len(users) != 0):
            for user in users:
                name = user.username
                if(name == username):
                    user = User.objects.get(username=username)
                    data = json.loads(request.body.decode("utf-8"))
                    search_id = data.get('search_id')
                    provider = data.get('provider')
                    aoi = data.get('aoi')
                    products = data.get('products')
                    est_cost = data.get('est_cost')
                    curr_unit = data.get('curr_unit')

                    data = {
                        "search_id" : search_id,
                        "provider" : provider,
                        "aoi" : aoi,
                        "products" : products,
                        "est_cost" : est_cost,
                        "curr_unit" : curr_unit,
                    }

                    search = Search.objects.create(**data,user=user)

                    data = {
                        "message": f"New Search Results with id {search.search_id} added for User : {user.username}"
                    }
                    status = 201
                    break
                else:
                    data = {
                        "message": f"No such User : {username} exists"
                    }
                    status = 400
        else:
            data = {
                        "message": f"No such User : {username} exists"
            }
            status = 400
        
        return JsonResponse(data, status=status)
    
    
    def get(self, request, username):
        users = User.objects.all()
        if(len(users) != 0):
            for user in users:
                name = user.username
                if(name == username):
                    user = User.objects.get(username=username)
                    items = list(Search.objects.filter(user=user.id))
                    items_count = len(items)
                    print(items)
                    if(items_count != 0):
                        items_data = []
                        for item in items:
                            items_data.append({
                                "search_id" : item.search_id,
                                "provider" : item.provider,
                                "aoi" : item.aoi,
                                "products" : item.products,
                                "est_cost" : item.est_cost,
                                "curr_unit" : item.curr_unit,
                            })

                        data = {
                            'searches': items_data,
                            'search_count': items_count,
                        }
                        status = 200
                        break
                    else:
                        data = {
                        "message": f"No Saved Searches found for user : {user.username}"
                        }
                        status = 400
                        break
                else:
                    data = {
                        "message": f"No such User : {user.username} exists"
                    }
                    status = 400
        else:
            data = {
                        "message": f"No such User : {username} exists"
            }
            status = 400

        return JsonResponse(data,status=status)
    
    def delete(self, request, username):
        users = User.objects.all()
        if(len(users) != 0):
            for user in users:
                name = user.username
                if(name == username):
                    user = User.objects.get(username=username)
                    items = list(Search.objects.filter(user=user.id))
                    items_count = len(items)
                    print(items)
                    if(items_count != 0):
                        items_data = []
                        for item in items:
                            item.delete()

                        data = {
                            "message": f"All Saved Searches deleted for user : {user.username}"
                        }
                        status = 202
                        break
                    else:
                        data = {
                        "message": f"No Saved Searches found for user : {user.username}"
                        }
                        status = 400
                        break
                else:
                    data = {
                        "message": f"No such User : {user.username} exists"
                    }
                    status = 400
        else:
            data = {
                        "message": f"No such User : {username} exists"
            }
            status = 400

        return JsonResponse(data,status=status)
    
    
    
class UpdateSavedSearchView(APIView):
    permission_classes = [IsAuthenticated]
    
    def post(self, request, username, search_id):
        users = User.objects.all()
        if(len(users) != 0):
            for user in users:
                name = user.username
                if(name == username):
                    user = User.objects.get(username=username)
                    items = list(Search.objects.filter(user=user.id))
                    if(len(items) != 0):
                        for item in items:
                            data = json.loads(request.body.decode("utf-8"))
                            item_id = item.search_id
                            if(item_id == search_id):
                                item = Search.objects.get(search_id=search_id)
                                if("provider" in data):
                                    item.provider = data["provider"]
                                if("aoi" in data):
                                    item.aoi = data["aoi"]
                                if("products" in data):
                                    item.products = data["products"]
                                if("est_cost" in data):
                                    item.est_cost = data["est_cost"]
                                if("curr_unit" in data):
                                    item.provider = data["curr_unit"]

                                item.save()

                                data = {
                                    "message": f"Saved Search Results with id {search_id} has been updated for User : {user.username}"
                                }
                                status = 201
                                break
                            else:
                                data = {
                                    "message": f"No such Saved Search : {search_id} exists for user {username}"
                                }
                                status = 400
                    else:
                                data = {
                                    "message": f"No Saved Searches : found for user {username}"
                                }
                                status = 400
                else:
                    data = {
                        "message": f"No such User : {username} exists"
                    }
                    status = 400
        else:
            data = {
                        "message": f"No such User : {username} exists"
            }
            status = 400
        
        return JsonResponse(data, status=status)
    
    
    def get(self, request, username, search_id):
        users = User.objects.all()
        if(len(users) != 0):
            for user in users:
                name = user.username
                if(name == username):
                    user = User.objects.get(username=username)
                    items = list(Search.objects.filter(user=user.id))
                    if(len(items) != 0):
                        for item in items:
                            data = json.loads(request.body.decode("utf-8"))
                            item_id = item.search_id
                            if(item_id == search_id):
                                result_data = []
                                item = Search.objects.get(search_id=search_id)
                                result_data.append({
                                    "search_id" : item.search_id,
                                    "provider" : item.provider,
                                    "aoi" : item.aoi,
                                    "products" : item.products,
                                    "est_cost" : item.est_cost,
                                    "curr_unit" : item.curr_unit,
                                })
                                status = 200
                                break
                            else:
                                result_data = {
                                    "message": f"No such Saved Search : {search_id} exists for user {username}"
                                }
                                status = 400
                    else:
                                result_data = {
                                    "message": f"No Saved Searches : found for user {username}"
                                }
                                status = 400
                else:
                    result_data = {
                        "message": f"No such User : {username} exists"
                    }
                    status = 400
        else:
            result_data = {
                        "message": f"No such User : {username} exists"
            }
            status = 400
        
        return JsonResponse(result_data, status=status)
    
    def get(self, request, username, search_id):
        users = User.objects.all()
        if(len(users) != 0):
            for user in users:
                name = user.username
                if(name == username):
                    user = User.objects.get(username=username)
                    items = list(Search.objects.filter(user=user.id))
                    if(len(items) != 0):
                        for item in items:
                            item_id = item.search_id
                            if(item_id == search_id):
                                item = Search.objects.get(search_id=search_id)
                                item.delete()
                                result_data = {
                                    "message": f"Saved Search : {search_id} has been deleted for user {username}"
                                }
                                status = 202
                                break
                            else:
                                result_data = {
                                    "message": f"No such Saved Search : {search_id} exists for user {username}"
                                }
                                status = 400
                    else:
                                result_data = {
                                    "message": f"No Saved Searches : found for user {username}"
                                }
                                status = 400
                else:
                    result_data = {
                        "message": f"No such User : {username} exists"
                    }
                    status = 400
        else:
            result_data = {
                        "message": f"No such User : {username} exists"
            }
            status = 400
        
        return JsonResponse(result_data, status=status)
    
    
    
class OpenSearchView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, provider):
        allProviders = Provider.objects.all()
        if(len(allProviders) == null):
            json_response = {
                        "message": f"Provider {provider} does not exist"
                    }
            status = 400
        else:
            provider = Provider.objects.get(provider_name=provider)
            if(provider.provider_name == 'airbus'):
                subscriptions = list(Subscriptions.objects.filter(provider=provider.id))
                if(len(subscriptions) != 0):
                    for subscription in subscriptions:
                        if(subscription.type == 'search'):
                            item = Subscriptions.objects.get(subscription_id=subscription.subscription_id)
                            info = subscription.serviceinfo
                            links = provider.links
                            baseUrl = links['searchdomain']
                            url = baseUrl
                            authurl = links['authdomain']
                            
                            securityheader = {
                                "apikey" : provider.api_key,
                                "grant_type" : "api_key",
                                "client_id" : "IDP"
                            }
                            authresponse = requests.post(authurl, data=securityheader)
                            
                            # time.sleep(5)
                            # print(authresponse.text)
                            auth_response = json.loads(authresponse.text)
                            token = auth_response['access_token']
                            headers = {
                                "Authorization": "Bearer " + token
                            }
                            body = info['bodyjson']
                            response = requests.get(url, headers=headers)
                            # print(response.text)
                            json_response = json.loads(response.text)
                            status = 200
                            break
                        else:
                            json_response = {
                                "message": f"Provider {provider} does not have search subscription"
                            }
                            status = 400
                else:
                        json_response = {
                            "message": f"Can not find any subscription for Provider {provider}"
                        }
                        status = 400
        return JsonResponse(json_response,status=status)