"""micronet URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from django.conf.urls.static import static
# from django.conf.urls import url
from . import settings
from django.views.generic import TemplateView
from django.contrib.auth import views as auth_views


from micronet_app.views import password


urlpatterns = [
    path('admin/', admin.site.urls),
    # path('', TemplateView.as_view(template_name="home.html"), name='home'),
    path('micronet/password_reset/', include('django_rest_passwordreset.urls', namespace='password_reset')),
    path('micronet/', include('micronet_app.urls')),
    path('reset/done/', TemplateView.as_view(template_name='commons/password-reset/password_reset_confirm.html'), name='password_reset_confirm'),
    path('', TemplateView.as_view(template_name='home.html'), name='home'), 
    path('login/', auth_views.LoginView.as_view(redirect_authenticated_user=True, template_name='commons/login.html'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(next_page='home'), name='logout'),
    path('password_reset/done/', auth_views.PasswordResetDoneView.as_view(template_name='commons/password-reset/password_reset_confirm.html'), name='password_reset_done'),
    path('reset/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(template_name="main/password/password_reset_confirm.html"), name='password_reset_confirm'),
    path('reset/done/', auth_views.PasswordResetCompleteView.as_view(template_name='main/password/password_reset_complete.html'), name='password_reset_complete'),      
    path("password_reset/", password.password_reset_request, name="password_reset")
]

# if settings.DEBUG:
#     urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)