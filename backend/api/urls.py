from django.urls import path, include
from rest_framework import routers
from . import views

#router = routers.DefaultRouter()
#router.register(r'models', views.ModelView, 'model')

urlpatterns = [
    #path("", include(router.urls)),
    path("", views.index, name="index"),
]