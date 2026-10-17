from django.urls import path
from . import views
urlpatterns=[path('',views.banking_home,name='banking_home')]
