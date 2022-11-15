"""books URL Configuration

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
from django.urls import path, include
from .views import book_details, book_list, BookApiView,BookDetails,GenericApiView,BookViewSets
from rest_framework.urlpatterns import format_suffix_patterns
from rest_framework.routers import DefaultRouter
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)
from .views import MyTokenObtainPairView

router = DefaultRouter()
router.register('books', BookViewSets,basename="books")

urlpatterns = [
    path('admin/', admin.site.urls),

    # function based api view
    path('api/books/', book_list),
    path('api/books/<int:id>', book_details),

    # class based api view
    path('class/books/', BookApiView.as_view()),
    path('class/books/<int:id>', BookDetails.as_view()),

    # generic api view
    path('generic/books/', GenericApiView.as_view()),
    path('generic/books/<int:id>', GenericApiView.as_view()),

    # viewsets
    path('viewsets/<int:id>', include(router.urls)),
    path('viewsets/', include(router.urls)),

    # jwt token
    path('api/token/', MyTokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),

]

# urlpatterns = format_suffix_patterns(urlpatterns) 