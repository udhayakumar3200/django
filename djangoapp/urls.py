from django.urls import path 
from .import views
from .views import ProfileApi

urlpatterns = [
    path("profile/", ProfileApi.as_view())
    # path('',views.getData),
    # path('create',views.addUser),
    # path('read/<str:pk>',views.getUser),
    # path('update/<str:pk>',views.updateUser),
    # path('delete/<str:pk>',views.deleteUser)
]
