import json
import profile

import requests
from django.contrib.auth.models import User
from django.contrib.sites.shortcuts import get_current_site
from django.http import JsonResponse
from django.shortcuts import HttpResponseRedirect, redirect, render
from django.template.loader import render_to_string
from django.utils.decorators import method_decorator
from django.utils.encoding import force_bytes,smart_str, force_str,smart_bytes,DjangoUnicodeDecodeError
from django.utils.http import urlsafe_base64_decode, urlsafe_base64_encode
from django.views import View
from django.views.decorators.csrf import csrf_exempt
from micronet_app.serializers import MyTokenObtainPairSerializer,RegisterSerializer, ChangePasswordSerializer,SetNewPasswordSerializer,ResetPasswordEmailRequestSerializer
from rest_framework import generics
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.views import APIView
from rest_framework_simplejwt.views import TokenObtainPairView
from sqlalchemy import null, true
from ..forms import UserForgotPasswordForm,UserPasswordResetForm
from django.contrib.auth import update_session_auth_hash
from django.views.decorators.http import require_http_methods
from django.urls import reverse
from ..models.customer import Profile
from ..tokens  import password_reset_token
from django.http import HttpResponsePermanentRedirect
from django.contrib.auth.tokens import PasswordResetTokenGenerator
import os


class CustomRedirect(HttpResponsePermanentRedirect):

    allowed_schemes = [os.environ.get('APP_SCHEME'), 'http', 'https']

@method_decorator(csrf_exempt, name='dispatch')
class Signup(generics.CreateAPIView):
    permission_classes = [IsAuthenticated]
    # queryset = User.objects.all()
    # serializer_class = RegisterSerializer

    def get(self, request):
        # customers_count = Customer.objects.count()
        customers_count = User.objects.count()
        customers_data = []
        
        customers = User.objects.all()
        print(customers)
        for customer in customers:
            customers_data.append({
                'username': customer.username,
                'first_name': customer.first_name,
                'last_name': customer.last_name,
                'email': customer.email,
                'is_active' : customer.is_active,
                'date_joined' : customer.date_joined
                
            })

        data = {
            'customers': customers_data,
            'count': customers_count,
        }

        return JsonResponse(data)


class MyObtainTokenPairView(TokenObtainPairView):
    # permission_classes = (AllowAny,)
    serializer_class = MyTokenObtainPairSerializer
    
class RegisterView(generics.CreateAPIView):
    queryset = User.objects.all()
    permission_classes = (IsAuthenticated,)
    serializer_class = RegisterSerializer



@method_decorator(csrf_exempt, name='dispatch')
class CustomerUpdate(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, username):
        data = json.loads(request.body.decode("utf-8"))
        user = User.objects.get(username=username)

        user.first_name = data['first_name']
        user.last_name = data['last_name']
        user.save()

        data = {
            'message': f'User {username} has been updated'
        }

        return JsonResponse(data)

    
    def get(self, request, username):
        customer = User.objects.get(username=username)
        data = {
           'first_name': customer.first_name,
            'last_name': customer.last_name,
            'email': customer.email,
        }

        return JsonResponse(data)


from django.contrib import messages
from django.contrib.auth import login
from django.contrib.auth.models import User
from django.shortcuts import redirect, render
from django.urls import reverse_lazy
# from django.utils.encoding import force_text
from django.utils.encoding import force_str
from django.utils.http import urlsafe_base64_decode
from django.views.generic import UpdateView, View

from ..forms import ProfileForm, SignUpForm
from ..tokens import account_activation_token


class ActivateAccount(View):

    def get(self, request, uidb64, token, *args, **kwargs):
        try:
            uid = force_str(urlsafe_base64_decode(uidb64))
            user = User.objects.get(pk=uid)
        except (TypeError, ValueError, OverflowError, User.DoesNotExist):
            user = None

        if user is not None and account_activation_token.check_token(user, token):
            user.is_active = True
            user.profile.emailConfirmed = True
            user.save()
            login(request, user)
            messages.success(request, ('Your account have been confirmed.'))
            return redirect('home')
        else:
            messages.warning(request, ('The confirmation link was invalid, possibly because it has already been used.'))
            return redirect('home')


#Edit Profile View
class ProfileView(UpdateView):
    model = User
    form_class = ProfileForm
    success_url = reverse_lazy('home')
    template_name = 'commons/profile.html'

import datetime
from datetime import timedelta

from django.contrib.auth.models import User
from django.http import Http404
from rest_framework import status
from rest_framework.response import Response


class TempUsers(APIView):
    permission_classes = [IsAuthenticated]


    def get(self, request):
        users = User.objects.all()
        # profile = Profile.objects.get()
        customers_data = []
        
        customers = User.objects.all()
        print(customers)
        for user in users:
            if user.is_active == False:
                profile = Profile.objects.get(user=user.id)
                customers_data.append({
                    'username': user.username,
                    'phone_number': profile.phone_number,
                    'address': profile.address,
                    'email_confirmed': profile.email_confirmed
                
                })

        data = {
            'Temp Users': customers_data
        }

        return JsonResponse(data)
        # for user in users:
        #     if user.is_active == False:
        #         # customer = User.objects.get(username=username)
                
        #         return JsonResponse({
        #         'username': user.username,
        #         'phone_number': profile.phone_number,
        #         'address': profile.address,
        #         'email_confirmed': profile.email_confirmed
        #         })



    def delete(self, request, *args, **kwargs):
        users = User.objects.all()
        for user in users:
            register_time = user.date_joined
            # ten_minutes_later = (register_time + timedelta(hours=0.016))
            # if ten_minutes_later == datetime.datetime.now():
            if user.is_active == False:
                # user.groups.delete()
                # user.profile.delete()
                user.delete()
        
        return Response({"result":"user delete"})

@method_decorator(csrf_exempt, name='dispatch')
class ProfileUpdate(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, username):
        data = json.loads(request.body.decode("utf-8"))
        customer = User.objects.get(username=username)
        print(customer.id)
        profile = Profile.objects.get(user_id=customer.id)
        profile.phoneNumber = data['phone_number']
        profile.address = data['address']
        profile.save()

        data = {
            'message': f' {username} profile has been updated'
        }

        return JsonResponse(data)

    def get(self, request, username):
        customer = User.objects.get(username=username)
        profile = Profile.objects.get(user_id=customer.id)
        data = {
            'parentUsername': customer.parentUsername,
            'first_name': customer.first_name,
            'last_name': customer.last_name,
            'email': customer.email,
           'phoneNumber': profile.phone_number,
           'address': profile.address,
           'emailConfirmed': profile.emailConfirmed
        }

        return JsonResponse(data)
       
class ChangePasswordView(generics.UpdateAPIView):
        """
        An endpoint for changing password.
        """
        serializer_class = ChangePasswordSerializer
        model = User
        # permission_classes = (IsAuthenticated,)

        def get_object(self, queryset=None):
            obj = self.request.user
            return obj

        def update(self, request, *args, **kwargs):
            self.object = self.get_object()
            serializer = self.get_serializer(data=request.data)

            if serializer.is_valid():
                # Check old password
                if not self.object.check_password(serializer.data.get("old_password")):
                    return Response({"old_password": ["Wrong password."]}, status=status.HTTP_400_BAD_REQUEST)
                # set_password also hashes the password that the user will get
                self.object.set_password(serializer.data.get("new_password"))
                self.object.save()
                response = {
                    'status': 'success',
                    'code': status.HTTP_200_OK,
                    'message': 'Password updated successfully',
                    'data': []
                }
                return Response(response)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        
        def post(self,request):
            msg = ''
            if request.method == "POST":
                form = UserForgotPasswordForm(request.POST)
                if form.is_valid():
                    email = request.POST.get('email')
                    tempurl = request.POST.get('tempurl')

                    qs = User.objects.filter(email=email)
                    site = get_current_site(request)
                    print (qs)

                    if len(qs) > 0:
                        
                        user = qs[0]
                        user.is_active = False  # User needs to be inactive for the reset password duration
                        user.profile.reset_password = True
                        user.save()

                        url = "https://api.sendinblue.com/v3/smtp/email"

                      
                        payload = json.dumps({
                        "sender": {
                            "name": "6Simplex",
                            "email": "butler@6simplex.co.in"
                        },
                        "to": [
                            {
                            "email": email
                            }
                        ],
                        "subject": "Verification Link",
                        "textContent": render_to_string('commons/password-reset/password_reset_mail.html', {'user': user,'domain': tempurl,'uid': urlsafe_base64_encode(force_bytes(user.pk)),'token': password_reset_token.make_token(user),})
                        })
                        headers = {
                            'accept': 'application/json',
                            'api-key': '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',
                            'content-type': 'application/json'
                        }

                        response = requests.request("POST", url, headers=headers, data=payload)
                        print(response.text)
                
            return render(request, 'commons/password-reset/password_reset_done.html', {'form': UserForgotPasswordForm, 'msg': msg})


# class Reset(View):
#     # @require_http_methods(["GET", "POST"])
#     def get(self, request, uidb64, token, *args, **kwargs):
        
#         # if request.method == 'POST':
#             try:
#                 uid = force_str(urlsafe_base64_decode(uidb64))
#                 user = User.objects.get(pk=uid)
#             except (TypeError, ValueError, OverflowError, User.DoesNotExist) as e:
#                 messages.add_message(request, messages.WARNING, str(e))
#                 user = None

#             if user is not None and password_reset_token.check_token(user, token):
#                 form = UserPasswordResetForm(user=user, data=request.POST)
#                 if form.is_valid():
#                     form.save()
#                     update_session_auth_hash(request, form.user)

#                     user.is_active = True
#                     user.profile.reset_password = False
#                     user.save()
#                     messages.add_message(request, messages.SUCCESS, 'Password reset successfully.')
#                     return redirect('login')
#                 else:
#                     context = {
#                         'form': form,
#                         'uid': uidb64,
#                         'token': token
#                     }
#                     messages.add_message(request, messages.WARNING, 'Password could not be reset.')
#                     return render(request, 'commons/password-reset/password_reset_confirm.html', context)
#             else:
#                 messages.add_message(request, messages.WARNING, 'Password reset link is invalid.')
#                 messages.add_message(request, messages.WARNING, 'Please request a new password reset.')

#             try:
#                 uid = force_str(urlsafe_base64_decode(uidb64))
#                 user = User.objects.get(pk=uid)
#             except (TypeError, ValueError, OverflowError, User.DoesNotExist) as e:
#                 messages.add_message(request, messages.WARNING, str(e))
#                 user = None

#             if user is not None and password_reset_token.check_token(user, token):
#                 context = {
#                     'form': UserPasswordResetForm(user),
#                     'uid': uidb64,
#                     'token': token
#                 }
#                 return render(request, 'commons/password-reset/password_reset_confirm.html', context)
#             else:
#                 messages.add_message(request, messages.WARNING, 'Password reset link is invalid.')
#                 messages.add_message(request, messages.WARNING, 'Please request a new password reset.')

#             return redirect('home')


           


class RequestPasswordResetEmail(generics.GenericAPIView):
    serializer_class = ResetPasswordEmailRequestSerializer

    def post(self, request,):
        serializer = self.serializer_class(data=request.data)

        email = request.data.get('email')
        tempurl = request.data.get('tempurl')
        

        if User.objects.filter(email=email).exists():
            user = User.objects.get(email=email)
            uidb64 = urlsafe_base64_encode(smart_bytes(user.id))
            token = PasswordResetTokenGenerator().make_token(user)
            current_site = get_current_site(
                request=request).domain
            relativeLink = reverse(
                'password-reset-confirm', kwargs={'uidb64': uidb64, 'token': token})

            redirect_url = tempurl
            absurl = 'http://'+current_site + relativeLink
            email_body = 'Hello, \n Use link below to reset your password  \n' + \
                absurl
            
            url = "https://api.sendinblue.com/v3/smtp/email"

            payload = json.dumps({
            "sender": {
                "name": "6Simplex",
                "email": "butler@6simplex.co.in"
            },
            "to": [
                {
                "email": user.email
                # "name": validated_data.get('first_name+last_name')
                }
            ],
            "subject": "Password Reset Link",
            "textContent": email_body
            })
            headers = {
                'accept': 'application/json',
                'api-key': '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',
                'content-type': 'application/json'
            }

            response = requests.request("POST", url, headers=headers, data=payload)
            print(response.text)
        return Response({'success': 'We have sent you a link to reset your password',
                          'link': absurl }, status=status.HTTP_200_OK)


class PasswordTokenCheckAPI(generics.GenericAPIView):
    serializer_class = SetNewPasswordSerializer

    def get(self, request, uidb64, token):

        # redirect_url = request.GET.get('redirect_url')

        try:
            id = smart_str(urlsafe_base64_decode(uidb64))
            user = User.objects.get(id=id)

            if not PasswordResetTokenGenerator().check_token(user, token):
                return Response({'error': 'Token is not valid, please request a new one'}, status=status.HTTP_400_BAD_REQUEST)

            return Response({'success': True, 'message': 'credentials Valid', 'uidb64': uidb64,'token': token},status=status.HTTP_200_OK)

            
            #     if len(redirect_url) > 3:
            #         return CustomRedirect(redirect_url+'?token_valid=False')
            #     else:
            #         return CustomRedirect(os.environ.get('FRONTEND_URL', '')+'?token_valid=False')

            # if redirect_url and len(redirect_url) > 3:
            #     return CustomRedirect(redirect_url+'?token_valid=True&message=Credentials Valid&uidb64='+uidb64+'&token='+token)
            # else:
            #     return CustomRedirect(os.environ.get('FRONTEND_URL', '')+'?token_valid=False')

        except DjangoUnicodeDecodeError as identifier:
            # try:
            if not PasswordResetTokenGenerator().check_token(user):
                return Response({'error': 'Token is not valid, please request a new one'}, status=status.HTTP_400_BAD_REQUEST)
                    
            # except UnboundLocalError as e:
                



class SetNewPasswordAPIView(generics.GenericAPIView):
    serializer_class = SetNewPasswordSerializer

    def patch(self, request):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        return Response({'success': True, 'message': 'Password reset success'}, status=status.HTTP_200_OK)




class DeleteAccount(APIView):
    permission_classes = [IsAuthenticated]
    def delete(self, request, username):
        user=self.request.user
        user.delete()

        return Response({"result":"user delete"})


