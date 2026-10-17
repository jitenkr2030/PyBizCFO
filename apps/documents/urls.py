from django.urls import path
from . import views
urlpatterns=[path('',views.documents_home,name='documents_home')]
