from . import views
from django.urls import path
from django.contrib import admin
from django.urls import path, include
from django.urls import path
from django.conf import settings
from django.conf.urls.static import static
from . import views
from django.urls import path
from django.conf import settings
from django.conf.urls.static import static
from .views import RegisterUser, LoginUser, logout_user


urlpatterns = [
    path('', views.index, name='index'),
    path('', views.upload, name='upload'),
    path('reg', RegisterUser.as_view(), name='reg'),
    path('auth', LoginUser.as_view(), name='auth'),
    path('logout', logout_user, name='logout'),
    path('profile', views.profile, name='profile'),
    path('upload-file', views.uploadFile, name="uploadFile")
]

if settings.DEBUG:
    urlpatterns += static(
        settings.MEDIA_URL,
        document_root = settings.MEDIA_ROOT
    )
