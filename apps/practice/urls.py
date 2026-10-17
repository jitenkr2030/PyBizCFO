from django.urls import path
from . import views
urlpatterns=[path('',views.practice_home,name='practice_home')]
