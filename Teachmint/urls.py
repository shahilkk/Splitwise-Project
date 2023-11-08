
from django.contrib import admin
from django.urls import path,include
from django.contrib.staticfiles.urls import static, staticfiles_urlpatterns
from django.conf.urls.static import static
from django.conf import settings
from rest_framework_simplejwt import views as jwt_views 


urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('api.urls')),
    path('web/',include('web.urls')),
    path('auth/', include('djoser.urls')),
    path('token/', jwt_views.TokenObtainPairView.as_view(),name ='token_obtain_pair'), 
    path('token/refresh/', jwt_views.TokenRefreshView.as_view(),name ='token_refresh'),
]+static(settings.MEDIA_URL, document_root= settings.MEDIA_ROOT)
