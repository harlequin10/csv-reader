from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('analytics/', views.analytics, name='analytics'),
    path('clean-data/', views.clean_data, name='clean_data'),
    
]
