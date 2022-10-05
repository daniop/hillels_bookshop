"""core URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.1/topics/http/urls/
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
from django.contrib.auth.views import PasswordResetCompleteView, PasswordResetConfirmView, PasswordResetDoneView,\
    PasswordResetView
from django.urls import include, path

from shop import views

urlpatterns = (
    path('admin/', admin.site.urls),
    path('accounts/password_change/', views.PasswordsChangeViewCustom.as_view(), name='password_change'),
    path('accounts/password_change/success/', views.password_success, name='password_success'),
    path("accounts/", include("django.contrib.auth.urls")),
    path("accounts/my_profile/", views.UserProfile.as_view(), name="profile"),
    path("accounts/signup/", views.SignUpView.as_view(), name="signup"),
    path("accounts/update_profile/", views.UpdateProfile.as_view(), name="update_profile"),
    path(
        'accounts/password_reset/',
        PasswordResetView.as_view(template_name='registration/password_reset_form.html'),
        name='password_reset'
    ),
    path(
        'accounts/password_reset_done/',
        PasswordResetDoneView.as_view(template_name='registration/password_reset_done.html'),
        name='password_reset_done'
    ),
    path(
        'accounts/password_reset/<uidb64>/<token>/',
        PasswordResetConfirmView.as_view(template_name='registration/password_reset_confirm.html'),
        name='password_reset_confirm'
    ),
    path(
        'accounts/password_reset_complete/',
        PasswordResetCompleteView.as_view(template_name='registration/password_reset_complete.html'),
        name='password_reset_complete'
    ),
    path('cart/', include('cart.urls', namespace='cart')),
    path('orders/', include('orders.urls', namespace='orders')),
    path('', include('shop.urls', namespace='shop')),
    path('__debug__/', include('debug_toolbar.urls')),
)
