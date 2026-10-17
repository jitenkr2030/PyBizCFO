from django.contrib import admin
from django.urls import path, include
from django.contrib.auth import views as auth_views
from apps.core import views

urlpatterns = [
    path("admin/", admin.site.urls),
    path("accounts/login/", auth_views.LoginView.as_view(template_name="registration/login.html"), name="login"),
    path("accounts/logout/", auth_views.LogoutView.as_view(), name="logout"),
    path("", views.dashboard, name="dashboard"),
    path("organizations/", include("apps.organizations.urls")),
    path("accounting/", include("apps.accounting.urls")),
    path("sales/", include("apps.sales.urls")),
    path("banking/", include("apps.banking.urls")),
    path("compliance/", include("apps.compliance.urls")),
    path("reports/", include("apps.reporting.urls")),
    path("portal/", include("apps.client_portal.urls")),
    path("practice/", include("apps.practice.urls")),
    path("documents/", include("apps.documents.urls")),
]
