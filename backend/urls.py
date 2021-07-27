from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from users.views import FacebookLogin

urlpatterns = [
    path('admin/', admin.site.urls),         
    path('accounts/', include('allauth.urls'), name='socialaccount_signup'),
    path('rest-auth/', include('dj_rest_auth.urls')),   
    # path('rest-auth/registration/account-confirm-email/<str:key>/', ConfirmEmailView.as_view()), 
    path('rest-auth/registration/', include('dj_rest_auth.registration.urls')),
    # path('rest-auth/account-confirm-email/', VerifyEmailView.as_view(), name='account_email_verification_sent'),
    # path('rest-auth/password/reset/confirm/<slug:uidb64>/<slug:token>/', PasswordResetConfirmView.as_view(), name='password_reset_confirm'),
    path('rest-auth/facebook/', FacebookLogin.as_view(), name='fb_login'),    
    path('api/items/', include('items.urls')),
    path('api/users/', include('users.urls')),   
    path('api/address/', include('addresses.urls')),   
    path('djrichtextfield/', include('djrichtextfield.urls'))    
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
