from django.urls import path
from . import views
urlpatterns=[path('',views.accounting_home,name='accounting_home'),path('journals/new/',views.journal_create,name='journal_create'),path('journals/<int:pk>/post/',views.journal_post,name='journal_post')]
