from django.urls import path
from . import views

#router = routers.DefaultRouter()
#router.register(r'models', views.ModelView, 'model')

urlpatterns = [
    #path("", include(router.urls)),
    path("", views.index, name="index"),
]