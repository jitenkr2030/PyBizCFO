from django.urls import path
from . import views
urlpatterns=[path('',views.compliance_home,name='compliance_home')]
