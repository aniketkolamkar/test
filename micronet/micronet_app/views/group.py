from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated, AllowAny,IsAdminUser
from ..serializers import GroupSerializer
from django.contrib.auth.models import Group, Permission
from rest_framework.response import Response
from django.core import serializers
# from rest_framework import serializers
from rest_framework import viewsets
from rest_framework import generics
import json
from django.http import JsonResponse


class UsersGroupCreateView(APIView):
    permission_classes = [IsAdminUser]

    def post(self , request , *args, **kwargs):
        data = request.data
        serializer = GroupSerializer(data = data)
        if serializer.is_valid():
            data = serializer.validated_data
            group = Group.objects.create(name = data.get('name'))
            try:
                permissions = data.get('permissions')
                auth_group = Group.objects.get('add_user')
                auth_group.permissions.add(*permissions)        
            except Exception as e:
                print("Error in creating")
            
            return Response({"status":"Role Created"},status=201)
        return Response(serializer.errors, status=400)

    
    def get(self, request):
        # customers_count = Customer.objects.count()
        group_count = Group.objects.count()
        Group_data = []
        Groups = Group.objects.all()
        # print(Groups)
        for group in Groups:
            permissions = group.permissions.all()
            print(permissions)
            permission_data=[]
            for permission in permissions:
                print(permission)
                permission_data.append(permission)
            print(permission_data)
            per_data = serializers.serialize('json', permission_data)
            Group_data.append({
                'name': group.name,
                'permissions': per_data  
            })
        print(Group_data)
        data = {
            'groups': Group_data,
            'count': group_count,
        }
        print(data)
        return JsonResponse(data)


class GetPerm(APIView):

    def get(self, request, *args, **kwargs):
        # permissions = group.permissions.all()(permissions=permissions)
        permissions = serializers.serialize('json', Permission.objects.all())
        return Response(permissions)

class GroupViewSet(generics.CreateAPIView):
    """
    API endpoint that allows groups to be viewed or edited.
    """
    queryset = Group.objects.all()
    serializer_class = GroupSerializer
    permission_classes = [IsAuthenticated]