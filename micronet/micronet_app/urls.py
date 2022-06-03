from django.contrib import admin
from django.urls import path
from .views.signup import Signup, ProfileView, RegisterView,TempUsers,CustomerUpdate, ProfileUpdate,ChangePasswordView,DeleteAccount,RequestPasswordResetEmail,PasswordTokenCheckAPI,SetNewPasswordAPIView
# from .views.login import Login, logout,ChangePasswordView
from .views.orders import OrderView,orderUpdate
from .views.search import SavedSearchView, OpenSearchView
from .views.group import GroupViewSet,UsersGroupCreateView,GetPerm
from .views.providers import Providers, ProviderUpdate
from .views.subscriptions import Subscription, SubscriptionUpdate
from .views.contracts import ContractsView, ContractUpdate
from .views.services import ServicesView, serviceUpdate
from .views.promotions import PromotionsView, promotionUpdate
from .middlewares.auth import  auth_middleware
#from .views.products import ProductView,ProductUpdate
# from .views.token import MyTokenObtainPairView
from django.urls import path
from .views.signup import ActivateAccount
from django.views.generic import TemplateView

from rest_framework_simplejwt.views import (
    TokenRefreshView,
)
from .views.signup import MyObtainTokenPairView

urlpatterns = [
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('customers/<str:username>/orders/', OrderView.as_view(), name='orders'),
    path('contracts', ContractsView.as_view()),
    path('contracts/payments', ContractsView.as_view()),
    path('customers/<str:username>/orders/', OrderView.as_view()),
    path('customers/<str:username>/orders/<int:order_id>', orderUpdate.as_view()),
    path('customers/', Signup.as_view()),
    path('roles/', UsersGroupCreateView.as_view()),
    path('providers/', Providers.as_view()),
    path('providers/<str:provider_name>', ProviderUpdate.as_view()),
    path('providers/<str:provider_name>/subscriptions/', Subscription.as_view()),
    path('providers/<str:provider_name>/subscriptions/<str:subscription_id>', SubscriptionUpdate.as_view()),
    path('providers/<str:provider_name>/contracts/', ContractsView.as_view()),
    path('providers/<str:provider_name>/contracts/<str:contract_id>', ContractUpdate.as_view()),
    path('services/', ServicesView.as_view()),
    path('services/<str:service_id>', serviceUpdate.as_view()),
    path('promotions/', PromotionsView.as_view()),
    path('promotions/<str:promotion_id>', promotionUpdate.as_view()),
    # path('customers/<str:username>', CustomerUpdate.as_view()),
    path('tempuser/', TempUsers.as_view()),
    path('customers/<str:username>', CustomerUpdate.as_view()),
    path('customers/profile/<str:username>', ProfileUpdate.as_view()),
    path('customers/profile/', ProfileUpdate.as_view()),
    path('user/<str:username>/searches', SavedSearchView.as_view()),
    path('providers/<str:provider>/searches', OpenSearchView.as_view()),
    path('GetPerm/', GetPerm.as_view(), name='auth_register'),
    path('login/', MyObtainTokenPairView.as_view(), name='token_obtain_pair'),
    path('login/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('register/', RegisterView.as_view(), name='auth_register'),
    path('password_update/', ChangePasswordView.as_view(), name='password_update'),
    path('profile/<int:pk>/', ProfileView.as_view(), name='profile'),
    path('activate/<uidb64>/<token>/', ActivateAccount.as_view(), name='activate'),
    path('user/<str:username>/delete/', DeleteAccount.as_view(), name='delete_user'),  
    path('passwordReset/', ChangePasswordView.as_view(), name='password_reset'), 
#     path('reset/<uidb64>/<token>/', Reset.as_view(), name='reset'),
#     path('reset/done/<uidb64>/<token>/', ResetConfirm.as_view(), name='resetDone'),
    path('request-reset-email/', RequestPasswordResetEmail.as_view(),
         name="request-reset-email"),
    path('password-reset/<uidb64>/<token>/',
         PasswordTokenCheckAPI.as_view(), name='password-reset-confirm'),
    path('password-reset-complete/', SetNewPasswordAPIView.as_view(),
         name='password-reset-complete')    
]

