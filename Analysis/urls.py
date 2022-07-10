from django.urls import path
from Analysis import views


urlpatterns = [
    path('',views.Home,name='Home'),
    path('list/',views.AllPrediction.as_view(),name='list_view'),
]