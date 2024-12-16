"""
URL configuration for app project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.1/topics/http/urls/
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
from django.conf import settings
from django.contrib import admin
from django.urls import path, include
from django.conf.urls.static import static

from berserk import views

from rest_framework.routers import DefaultRouter
from berserk.api import BerserkCharacterViewSet, BerserkCreatureViewSet, BerserkGeographyViewSet, BerserkArmyViewSet, BerserkArtifactViewSet, AlbumViewSet, UserProfileViewSet, UserViewSet, login_view, register_view

router = DefaultRouter()
router.register("berserk_characters", BerserkCharacterViewSet, basename = "berserk_characters")
router.register("berserk_creatures", BerserkCreatureViewSet, basename = "berserk_creatures")
router.register("berserk_geography", BerserkGeographyViewSet, basename = "berserk_geography")
router.register("berserk_army", BerserkArmyViewSet, basename = "berserk_army")
router.register("berserk_artifact", BerserkArtifactViewSet, basename = "berserk_artifact")
router.register("user-profile", UserProfileViewSet, basename="user-profile")
router.register("users", UserViewSet, basename="users")
router.register("album", AlbumViewSet, basename = "album")
router.register("export-excel", BerserkCharacterViewSet, basename = "export-excel")

urlpatterns = [
    path('', views.ShowBerserkCharactersView.as_view()),
    path('admin/', admin.site.urls),
    path('api/', include(router.urls)),
    path('api/login/', login_view, name='login'),
    path('api/register/', register_view, name='register'),
] + static(settings.MEDIA_URL, document_root = settings.MEDIA_ROOT)
